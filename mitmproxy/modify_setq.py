import struct
import unittest


EPS_MSID_A4 = 0
EPS_MSID_LETTER = 1
EPS_MSID_LEGAL = 2
EPS_MSID_A5 = 3
EPS_MSID_A6 = 4
EPS_MSID_B5 = 5
EPS_MSID_EXECUTIVE = 6
EPS_MSID_HALFLETTER = 7
EPS_MSID_PANORAMIC = 8
EPS_MSID_TRIM_4X6 = 9
EPS_MSID_4X6 = 10
EPS_MSID_5X8 = 11
EPS_MSID_8X10 = 12
EPS_MSID_10X15 = 13
EPS_MSID_200X300 = 14
EPS_MSID_L = 15
EPS_MSID_POSTCARD = 16
EPS_MSID_DBLPOSTCARD = 17
EPS_MSID_ENV_10_L = 18
EPS_MSID_ENV_C6_L = 19
EPS_MSID_ENV_DL_L = 20
EPS_MSID_NEWEVN_L = 21
EPS_MSID_CHOKEI_3 = 22
EPS_MSID_CHOKEI_4 = 23
EPS_MSID_YOKEI_1 = 24
EPS_MSID_YOKEI_2 = 25
EPS_MSID_YOKEI_3 = 26
EPS_MSID_YOKEI_4 = 27
EPS_MSID_2L = 28
EPS_MSID_ENV_10_P = 29
EPS_MSID_ENV_C6_P = 30
EPS_MSID_ENV_DL_P = 31
EPS_MSID_NEWENV_P = 32
EPS_MSID_MEISHI = 33
EPS_MSID_BUZCARD_89X50 = 34
EPS_MSID_CARD_54X86 = 35
EPS_MSID_BUZCARD_55X91 = 36
EPS_MSID_ALBUM_L = 37
EPS_MSID_ALBUM_A5 = 38
EPS_MSID_PALBUM_L_L = 39
EPS_MSID_PALBUM_2L = 40
EPS_MSID_PALBUM_A5_L = 41
EPS_MSID_PALBUM_A4 = 42
EPS_MSID_HIVISION = 43
EPS_MSID_KAKU_2 = 44
EPS_MSID_ENV_C4_P = 45
EPS_MSID_B6 = 46
EPS_MSID_KAKU_20 = 47
EPS_MSID_A5_24HOLE = 48
EPS_MSID_CHOKEI_40 = 52
EPS_MSID_QUADRAPLEPOSTCARD = 53
EPS_MSID_YOKEI_0 = 54
EPS_MSID_ENV_C5_P = 56
EPS_MSID_YOKEI_6 = 57
EPS_MSID_MEXICO_OFICIO = 58
EPS_MSID_OFICIO9 = 59
EPS_MSID_INDIAN_LEGAL = 60
EPS_MSID_A3NOBI = 61
EPS_MSID_A3 = 62
EPS_MSID_B4 = 63
EPS_MSID_USB = 64
EPS_MSID_11X14 = 65
EPS_MSID_B3 = 66
EPS_MSID_A2 = 67
EPS_MSID_USC = 68
EPS_MSID_10X12 = 69
EPS_MSID_12X12 = 70
EPS_MSID_SP1 = 71
EPS_MSID_SP2 = 72
EPS_MSID_SP3 = 73
EPS_MSID_SP4 = 74
EPS_MSID_SP5 = 75
EPS_MSID_16K = 76
EPS_MSID_8K = 77
EPS_MSID_SRA3 = 84
EPS_MSID_12X18 = 85
EPS_MSID_8_5X13 = 86
EPS_MSID_SQUARE_8_27 = 87
EPS_MSID_SQUARE_5 = 88
EPS_MSID_USER = 99
EPS_MSID_8X10_5 = 104
EPS_MSID_8_27X13 = 106
EPS_MSID_ENV_B5_P = 111
EPS_MSID_BANNER = 113
EPS_MSID_SQUARE_3_5 = 116
EPS_MSID_8X12 = 117
EPS_MSID_SQUARE_6 = 118
EPS_MSID_4X8 = 119
EPS_MSID_7X10 = 120
EPS_MSID_3_5X2 = 121
EPS_MSID_6X2 = 122
EPS_MSID_8X5 = 123
EPS_MSID_6X4 = 124
EPS_MSID_8X4 = 125
EPS_MSID_HALFCUT = 128
EPS_MSID_16X20 = 129
EPS_MSID_17X24 = 141
EPS_MSID_30X40CM = 150
EPS_MSID_40X60CM = 151
EPS_MSID_ARCH_A = 153
EPS_MSID_ARCH_B = 154
EPS_MSID_A3WNOBI = 157

paper_sizes = {
    (2976, 4209): EPS_MSID_A4,
    (3060, 3960): EPS_MSID_LETTER,
    (3060, 5040): EPS_MSID_LEGAL,
    (2098, 2976): EPS_MSID_A5,
    (1488, 2098): EPS_MSID_A6,
    (2580, 3643): EPS_MSID_B5,
    (2611, 3780): EPS_MSID_EXECUTIVE,
    (1980, 3060): EPS_MSID_HALFLETTER,
    (2976, 8419): EPS_MSID_PANORAMIC,
    (1610, 2330): EPS_MSID_TRIM_4X6,
    (1440, 2160): EPS_MSID_4X6,
    (1800, 2880): EPS_MSID_5X8,
    (2880, 3600): EPS_MSID_8X10,
    (1417, 2125): EPS_MSID_10X15,
    (3061, 4790): EPS_MSID_200X300,
    (1261, 1800): EPS_MSID_L,
    (1417, 2098): EPS_MSID_POSTCARD,
    (2835, 2098): EPS_MSID_DBLPOSTCARD,
    (3420, 1485): EPS_MSID_ENV_10_L,
    (2296, 1616): EPS_MSID_ENV_C6_L,
    (3118, 1559): EPS_MSID_ENV_DL_L,
    (3118, 1871): EPS_MSID_NEWEVN_L,
    (1701, 3331): EPS_MSID_CHOKEI_3,
    (1276, 2906): EPS_MSID_CHOKEI_4,
    (1701, 2494): EPS_MSID_YOKEI_1,
    (1389, 2098): EPS_MSID_YOKEI_3,
    (1488, 3331): EPS_MSID_YOKEI_4,
    (1800, 2522): EPS_MSID_2L,
    (1485, 3420): EPS_MSID_ENV_10_P,
    (1616, 2296): EPS_MSID_ENV_C6_P,
    (1559, 3118): EPS_MSID_ENV_DL_P,
    (1871, 3118): EPS_MSID_NEWENV_P,
    (1261, 779): EPS_MSID_MEISHI,
    (1261, 709): EPS_MSID_BUZCARD_89X50,
    (765, 1219): EPS_MSID_CARD_54X86,
    (780, 1290): EPS_MSID_BUZCARD_55X91,
    (1800, 2607): EPS_MSID_ALBUM_L,
    (2976, 4294): EPS_MSID_ALBUM_A5,
    (1800, 1260): EPS_MSID_PALBUM_L_L,
    (1800, 2521): EPS_MSID_PALBUM_2L,
    (2976, 2101): EPS_MSID_PALBUM_A5_L,
    (2976, 4203): EPS_MSID_PALBUM_A4,
    (1440, 2560): EPS_MSID_HIVISION,
    (3401, 4705): EPS_MSID_KAKU_2,
    (3245, 4592): EPS_MSID_ENV_C4_P,
    (1814, 2580): EPS_MSID_B6,
    (1276, 3189): EPS_MSID_CHOKEI_40,
    (2835, 4195): EPS_MSID_QUADRAPLEPOSTCARD,
    (2296, 3246): EPS_MSID_ENV_C5_P,
    (1389, 2693): EPS_MSID_YOKEI_6,
    (3060, 4825): EPS_MSID_MEXICO_OFICIO,
    (3046, 4465): EPS_MSID_OFICIO9,
    (3047, 4890): EPS_MSID_INDIAN_LEGAL,
    (4663, 6846): EPS_MSID_A3NOBI,
    (4209, 5953): EPS_MSID_A3,
    (3643, 5159): EPS_MSID_B4,
    (3960, 6120): EPS_MSID_USB,
    (3960, 5040): EPS_MSID_11X14,
    (5159, 7299): EPS_MSID_B3,
    (5953, 8419): EPS_MSID_A2,
    (6120, 7920): EPS_MSID_USC,
    (3600, 4320): EPS_MSID_10X12,
    (4320, 4320): EPS_MSID_12X12,
    (2976, 3827): EPS_MSID_SP1,
    (2976, 2112): EPS_MSID_SP2,
    (1417, 2409): EPS_MSID_SP3,
    (1843, 2580): EPS_MSID_SP4,
    (2721, 1871): EPS_MSID_SP5,
    (2764, 3827): EPS_MSID_16K,
    (3827, 5528): EPS_MSID_8K,
    (4535, 6378): EPS_MSID_SRA3,
    (4320, 6480): EPS_MSID_12X18,
    (3060, 4680): EPS_MSID_8_5X13,
    (2976, 2976): EPS_MSID_SQUARE_8_27,
    (1800, 1800): EPS_MSID_SQUARE_5,
    # {   EPS_MSID_USER,             0,    0,    0,    0, -36, -42,    0,    0 },
    (2880, 3780): EPS_MSID_8X10_5,
    (2976, 4678): EPS_MSID_8_27X13,
    (2494, 3543): EPS_MSID_ENV_B5_P,
    (4209, 12756): EPS_MSID_BANNER,
    (1260, 1260): EPS_MSID_SQUARE_3_5,
    (2880, 4320): EPS_MSID_8X12,
    (2160, 2160): EPS_MSID_SQUARE_6,
    (1440, 2880): EPS_MSID_4X8,
    (2522, 3600): EPS_MSID_7X10,
    (1261, 720): EPS_MSID_3_5X2,
    (2160, 720): EPS_MSID_6X2,
    (2880, 1800): EPS_MSID_8X5,
    (2160, 1440): EPS_MSID_6X4,
    (2880, 1440): EPS_MSID_8X4,
    (5040, 6120): EPS_MSID_HALFCUT,
    (5760, 7200): EPS_MSID_16X20,
    (6120, 8646): EPS_MSID_17X24,
    (4252, 5669): EPS_MSID_30X40CM,
    (5669, 8504): EPS_MSID_40X60CM,
    (3240, 4320): EPS_MSID_ARCH_A,
    (4663, 7923): EPS_MSID_A3WNOBI,
}


def get_paper_size_id(buf: bytes) -> int | None:
    j_setj = bytes(
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
        ]
    )
    j_setj_parameter_offset = 10

    j_setj_start = buf.find(j_setj)

    if j_setj_start != -1:
        width_start = j_setj_start + j_setj_parameter_offset + 2
        heigth_start = width_start + 4
        (width,) = struct.unpack(">H", buf[width_start : width_start + 2])
        (height,) = struct.unpack(">H", buf[heigth_start : heigth_start + 2])
        print(f"Paper size: {width}x{height}")
        return paper_sizes.get((width, height))
    else:
        return None


class ModifySetQ:
    def request(self, flow):
        if flow.request.method == "POST":
            print("detected POST")
            if bytes([0x02, 0x00, 0x00, 0x06]) in flow.request.content:
                print("detected Send-Document")
                content = flow.request.content
                before, sep, after = content.partition(
                    bytes([0x1B, 0x70, 0x00, 0x00, 0x00, 0x00, 0x73, 0x74, 0x74, 0x70])
                )
                if sep:
                    print("separator found")
                    # q-setq
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


addons = [ModifySetQ()]


class TestGetPaperSizeId(unittest.TestCase):
    def test_get_paper_size_id(self):
        buf = bytes(
            [
                0x00,
                0x05,
                0x00,
                0x1B,
                0x00,
                0x00,
                0x00,
                0x1B,
                0x28,
                0x52,
                0x06,
                0x00,
                0x00,
                0x45,
                0x53,
                0x43,
                0x50,
                0x52,
                0x1B,
                0x71,
                0x09,
                0x00,
                0x00,
                0x00,
                0x73,
                0x65,
                0x74,
                0x71,
                0x0C,
                0x02,
                0x00,
                0x00,
                0x00,
                0x00,
                0x03,
                0x00,
                0x00,
                0x1B,
                0x71,
                0x0A,
                0x00,
                0x00,
                0x00,
                0x73,
                0x65,
                0x74,
                0x69,
                0x01,
                0x01,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
                0x00,
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
                0xA0,
                0x00,
                0x00,
                0x10,
                0x71,
                0x00,
                0x2A,
                0x00,
                0x2A,
                0x00,
                0x00,
                0x0B,
                0x4C,
                0x00,
                0x00,
                0x10,
                0x1D,
                0x00,
                0x00,
                0x1B,
                0x70,
                0x00,
                0x00,
                0x00,
                0x00,
                0x73,
                0x74,
                0x74,
                0x70,
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
        self.assertEqual(get_paper_size_id(buf), EPS_MSID_A4)
