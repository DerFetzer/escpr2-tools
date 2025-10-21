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

import sys

from escpr2_tools.escpr_commands import COMMANDS, EscprCommand, EscprCommandUnknown


def main() -> int:
    if len(sys.argv) == 2:
        file_name = sys.argv[1]
        with open(file_name, "rb") as f:
            file_bytes = f.read()
        print_single(file_bytes)
    if len(sys.argv) == 3:
        ref_file_name = sys.argv[1]
        with open(ref_file_name, "rb") as f:
            ref_file_bytes = f.read()
        file_name = sys.argv[2]
        with open(file_name, "rb") as f:
            file_bytes = f.read()
        diff_two(ref_file_bytes, file_bytes)
    else:
        raise ValueError("Call this program with one or two binary files")

    return 0


def print_single(file_bytes: bytes):
    commands_dict = get_commands_dict(file_bytes)
    print_commands_dict(commands_dict)


def diff_two(ref_file_bytes: bytes, file_bytes: bytes):
    ref_commands_dict = get_commands_dict(ref_file_bytes)
    commands_dict = get_commands_dict(file_bytes)

    print("Reference:")
    print_commands_dict(ref_commands_dict)

    print("Other:")
    print_commands_dict(commands_dict)

    print("Reference vs. Other")
    diff_commands_dicts(ref_commands_dict, commands_dict)

    print()
    print("Other vs. Reference")
    diff_commands_dicts(commands_dict, ref_commands_dict)


def diff_commands_dicts(
    ref_commands_dict: dict[bytes, type[EscprCommand] | EscprCommandUnknown],
    commands_dict: dict[bytes, type[EscprCommand] | EscprCommandUnknown],
):
    for header, command in ref_commands_dict.items():
        if header not in commands_dict.keys():
            print(
                f"\n{command.get_command_description()} is not in commands dict\n{str(command)}"
            )
            continue
        elif command != commands_dict[header]:
            print(
                f"\nArguments differ for {command.get_command_description()}:\n{str(command)}\n{str(commands_dict[header])}"
            )
        else:
            print(
                f"\nArguments for {command.get_command_description()} are equal\n{str(command)}"
            )


def print_commands_dict(
    commands_dict: dict[bytes, type[EscprCommand] | EscprCommandUnknown],
):
    for _header, command in commands_dict.items():
        print(str(command))

        print()


def get_commands_dict(
    file_bytes: bytes,
) -> dict[bytes, type[EscprCommand] | EscprCommandUnknown]:
    commands_dict: dict[bytes, type[EscprCommand] | EscprCommandUnknown] = {}
    commands = file_bytes.split(b"\x1b")

    inside_data = False
    for command in commands:
        if inside_data:
            if b"ESCPR" in command:
                inside_data = False
            continue

        if len(command) == 0 or command[0] < 0x61 or command[0] > 0x7A:
            # non lowercase letter
            continue

        if command.startswith(b"d") or command.startswith(b"(d"):
            # data
            inside_data = True
            continue

        header = command[:9]
        params = command[9:50]

        cmd_class = COMMANDS.get(header)

        if cmd_class is not None:
            commands_dict[header] = cmd_class(params)
        else:
            commands_dict[header] = EscprCommandUnknown(header, params)

    return commands_dict
