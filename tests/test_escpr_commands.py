from escpr2_tools.escpr_commands import COMMANDS, EscprCommandJSetj, EscprCommandPSetn


def test_check_parameter_defs():
    for cmd in COMMANDS.values():
        print(cmd.NAME)
        cmd.check_parameter_defs()


def test_j_setj():
    data = bytes(
        [
            0x1B,
            0x6A,
            0x16,
            0x00,
            0x00,
            0x00,
            0x73,
            0x65,
            0x74,
            0x6A,
            0x00,
            0x00,
            0x0B,
            0x40,
            0x00,
            0x00,
            0x10,
            0xE0,
            0x00,
            0x54,
            0x00,
            0x54,
            0x00,
            0x00,
            0x0A,
            0x98,
            0x00,
            0x00,
            0x10,
            0x38,
            0x01,
            0x00,
        ]
    )
    cmd = EscprCommandJSetj(data[10:])
    print(cmd.__str__())
    assert cmd.PaperWidth == 2880
    assert cmd.__bytes__() == data


def test_p_setn():
    cmd = EscprCommandPSetn(b"\x01")
    print(cmd.__str__())
    assert cmd.NextPage == 1

def test_p_setn_empty():
    cmd = EscprCommandPSetn()
    print(cmd.__str__())
    assert cmd.NextPage == 0
