# escpr2-tools
# Copyright (C) 2025  DerFetzer
#
# This file is part of escpr2-tools.
#
# escpr2-tools is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later
# version.
#
# escpr2-tools is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# escpr2-tools. If not, see <https://www.gnu.org/licenses/>.
#

import argparse
import asyncio
import struct

from mitmproxy.options import Options

from escpr2_tools.constants import PAPER_SIZES
from escpr2_tools.decode_escpr import print_single
from mitmproxy.tools.dump import DumpMaster

from escpr2_tools.escpr_commands import (
    EscprCommandJSetj,
    EscprCommandMSeti,
    EscprCommandMSetm,
    EscprCommandPSttp,
    EscprCommandPSetq,
    EscprCommandUChku,
)


def get_paper_size_id(buf: bytes) -> int | None:
    j_setj_esc_header = EscprCommandJSetj.get_esc_command_header()

    j_setj_start = buf.find(j_setj_esc_header)

    if j_setj_start != -1:
        j_setj_param_start = j_setj_start + len(j_setj_esc_header)
        j_setj = EscprCommandJSetj(
            buf[
                j_setj_param_start : j_setj_param_start
                + EscprCommandJSetj.PARAMETER_LENGTH
            ]
        )
        width = j_setj.PaperWidth
        height = j_setj.PaperLength
        print(f"Paper size: {width}x{height}")
        return PAPER_SIZES.get((width, height))
    else:
        return None


class ModifySendDocument:
    def request(self, flow):
        if flow.request.method == "POST":
            print("detected POST")
            if bytes([0x01, 0x01, 0x00, 0x06]) in flow.request.content:
                # Win
                print("detected Send-Document IPPv1.1")
                content = flow.request.content
                print_single(content)
            if bytes([0x02, 0x00, 0x00, 0x06]) in flow.request.content:
                # Linux
                print("detected Send-Document IPPv2")
                content = flow.request.content
                print_single(content)

                before, sep, after = content.partition(
                    EscprCommandPSttp.get_esc_command_header()
                )
                if sep:
                    print("p-sttp found")
                    p_setq = EscprCommandPSetq()
                    p_setq.ColorPlane = 0x03
                    p_setq.LUT = 0x04
                    p_setq.GammaCorrect = 0xDC

                    content = before + sep + p_setq.__bytes__() + after

                before, sep, after = content.partition(
                    EscprCommandJSetj.get_esc_command_header()
                )
                if sep:
                    print("j-setj found")
                    paper_size_id = get_paper_size_id(content)
                    print(f"paper_size_id: {paper_size_id}")
                    if paper_size_id is None:
                        print("Could not determine paper size!")
                        flow.request.set_content(bytes())
                        return

                    # m-seti + m-setm + u-chku
                    # Works only with all three
                    m_seti = EscprCommandMSeti()

                    m_setm = EscprCommandMSetm()
                    m_setm.MediaSizeID = paper_size_id
                    m_setm.DocumentType = 0x63

                    u_chku = EscprCommandUChku()
                    u_chku.NonCheckPrintMode = 1

                    content = (
                        before
                        + m_seti.__bytes__()
                        + m_setm.__bytes__()
                        + u_chku.__bytes__()
                        + sep
                        + after
                    )
                flow.request.set_content(content)


addons = [ModifySendDocument()]


def main():
    parser = argparse.ArgumentParser(
        prog="escpr2-proxy",
        description="Spawns a proxy to inspect and manipulate escpr2 commands inside IPP.",
    )
    parser.add_argument("printer_address")
    parser.add_argument("local_address")
    args = parser.parse_args()

    proxy_mode = f"reverse:https://{args.printer_address}:631@{args.local_address}:631"

    try:
        asyncio.run(__start_proxy(proxy_mode))
    except KeyboardInterrupt:
        print("Stopping proxy...")


async def __start_proxy(proxy_mode: str):
    opts = Options(mode=[proxy_mode], ssl_insecure=True)
    proxy = DumpMaster(opts)
    proxy.addons.add(ModifySendDocument())

    print("Starting proxy...")
    await proxy.run()
    print("Stopping proxy...")
