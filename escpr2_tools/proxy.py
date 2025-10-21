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

from escpr2_tools.escpr_commands import EscprCommandJSetj, EscprCommandPSttp, EscprCommandPSetq


def get_paper_size_id(buf: bytes) -> int | None:
    j_setj_esc_header = EscprCommandJSetj.get_esc_command_header()
    j_setj_parameter_offset = 10

    j_setj_start = buf.find(j_setj_esc_header)

    if j_setj_start != -1:
        width_start = j_setj_start + j_setj_parameter_offset + 2
        heigth_start = width_start + 4
        (width,) = struct.unpack(">H", buf[width_start : width_start + 2])
        (height,) = struct.unpack(">H", buf[heigth_start : heigth_start + 2])
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
                    p_setq.parameters["ColorPlane"] = 0x03
                    p_setq.parameters["LUT"] = 0x04
                    p_setq.parameters["GammaCorrect"] = 0xDC

                    content = (
                        before
                        + sep
                        + bytes(
                            [
                                0x1B,
                                0x70,
                                0x0C,
                                0x00,
                                0x00,
                                0x00,
                                0x73,
                                0x65,
                                0x74,
                                0x71,
                                0x00,
                                0x03,
                                0x04,
                                0x00,
                                0xDC,
                                0x00,
                                0x00,
                                0x00,
                                0x00,
                                0x00,
                                0x00,
                                0x00,
                            ]
                        )
                        + after
                    )
                before, sep, after = content.partition(
                    bytes([0x1B, 0x6A, 0x16, 0x00, 0x00, 0x00, 0x73, 0x65, 0x74, 0x6A])
                )
                if sep:
                    print("2nd separator found")
                    paper_size_id = get_paper_size_id(content)
                    print(f"paper_size_id: {paper_size_id}")
                    if paper_size_id is None:
                        print("Could not determine paper size!")
                        flow.request.set_content(bytes())
                        return

                    # m-seti + m-setm + u-chku
                    # Works only with all three
                    content = (
                        before
                        + bytes(
                            [
                                0x1B,
                                0x6D,
                                0x01,
                                0x00,
                                0x00,
                                0x00,
                                0x73,
                                0x65,
                                0x74,
                                0x69,
                                0x00,
                            ]
                        )
                        + bytes(
                            [
                                0x1B,
                                0x6D,
                                0x07,
                                0x00,
                                0x00,
                                0x00,
                                0x73,
                                0x65,
                                0x74,
                                0x6D,
                                paper_size_id,  # paper size index: j-setj [2:4] -> width, [6:8] -> length
                                0x00,
                                0x00,
                                0x63,
                                0x00,
                                0x00,
                                0x00,
                            ]
                        )
                        + bytes(
                            [
                                0x1B,
                                0x75,
                                0x02,
                                0x00,
                                0x00,
                                0x00,
                                0x63,
                                0x68,
                                0x6B,
                                0x75,
                                0x01,
                                0x00,
                            ]
                        )
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
