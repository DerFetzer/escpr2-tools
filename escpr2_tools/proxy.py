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
from enum import Enum
import struct

from mitmproxy.options import Options

from escpr2_tools.constants import PAPER_LUT_AUTOMATIC, PAPER_SIZES
from escpr2_tools.decode_escpr import print_single
from mitmproxy.tools.dump import DumpMaster

from escpr2_tools.escpr_commands import (
    EscprCommandJSetj,
    EscprCommandMSeti,
    EscprCommandMSetm,
    EscprCommandPSttp,
    EscprCommandPSetq,
    EscprCommandQSetb,
    EscprCommandQSetq,
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


def get_media_type_id(buf: bytes) -> int | None:
    q_setq_esc_header = EscprCommandQSetq.get_esc_command_header()

    q_setq_start = buf.find(q_setq_esc_header)

    if q_setq_start != -1:
        q_setq_param_start = q_setq_start + len(q_setq_esc_header)
        q_setq = EscprCommandQSetq(
            buf[
                q_setq_param_start : q_setq_param_start
                + EscprCommandQSetq.PARAMETER_LENGTH
            ]
        )
        media_type_id = q_setq.MediaTypeID
        print(f"Media type id: {media_type_id}")
        return media_type_id
    else:
        return None


class PrintMode(Enum):
    Auto = 1
    CmOff = 2
    ABW = 3


class ModifySendDocument:
    def request(self, flow):
        mode = PrintMode.Auto

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
                    p_setq.GammaCorrect = 0xDC
                    match mode:
                        case PrintMode.Auto:
                            media_type_id = get_media_type_id(content)
                            if media_type_id is None:
                                raise ValueError("Could not get media type id")
                            p_setq.LUT = PAPER_LUT_AUTOMATIC.get(media_type_id, 6)
                        case PrintMode.CmOff:
                            p_setq.LUT = 0x04
                        case PrintMode.ABW:
                            p_setq.LUT = 0x07

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

                    q_setb = EscprCommandQSetb()
                    q_setb.MonoGamma = 0xDC

                    content = (
                        before
                        + (q_setb.__bytes__() if mode == PrintMode.ABW else bytes())
                        + m_seti.__bytes__()
                        + m_setm.__bytes__()
                        + u_chku.__bytes__()
                        + sep
                        + after
                    )
                print("Modified:")
                print_single(content)
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
