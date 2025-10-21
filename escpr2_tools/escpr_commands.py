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

import struct
from typing import override
from warnings import warn
import unittest


class EscprCommand:
    NAME: str = ""
    COMMAND_CLASS: str = ""
    PARAMETER_LENGTH: int = 0
    COMMAND_NAME: str = ""

    PARAMETER_DEFS: list[str | tuple[str, str]] = []

    @classmethod
    def get_command_header(cls) -> bytes:
        return (
            cls.COMMAND_CLASS[0].encode("ascii")
            + bytes([cls.PARAMETER_LENGTH, 0x00, 0x00, 0x00])
            + cls.COMMAND_NAME.encode("ascii")
        )

    @classmethod
    def get_esc_command_header(cls) -> bytes:
        return b"\x1b" + cls.get_command_header()

    @classmethod
    def check_parameter_defs(cls):
        calc_param_len = 0
        for parameter_def in cls.PARAMETER_DEFS:
            param_len = struct.calcsize(
                cls.__get_name_and_fmt_from_def(parameter_def)[1]
            )
            calc_param_len += param_len
        if calc_param_len != cls.PARAMETER_LENGTH:
            raise ValueError(
                f"PARAMETER_LENGTH does not match calculated: {cls.PARAMETER_LENGTH} != {calc_param_len}"
            )

    @classmethod
    def __get_name_and_fmt_from_def(cls, parameter_def: str | tuple[str, str]):
        if isinstance(parameter_def, str):
            parameter_name = parameter_def
            fmt = "B"
        elif isinstance(parameter_def, tuple) and len(parameter_def) == 2:
            parameter_name = parameter_def[0]
            fmt = parameter_def[1]
        else:
            raise RuntimeError(f"Invalid parameter definition: {parameter_def}")
        return parameter_name, fmt

    def __init__(self, params: bytes | None = None):
        self.check_parameter_defs()

        parameter_offset = 0

        self.raw_parameters: bytes = (
            params if params else bytes([0] * self.PARAMETER_LENGTH)
        )
        for parameter_def in self.PARAMETER_DEFS:
            parameter_name, fmt = self.__get_name_and_fmt_from_def(parameter_def)
            setattr(
                self,
                parameter_name,
                struct.unpack_from(
                    fmt, buffer=self.raw_parameters, offset=parameter_offset
                )[0],
            )

            parameter_offset += struct.calcsize(fmt)
        if parameter_offset != len(self.raw_parameters):
            warn(
                f"Unused bytes remaining: {self.raw_parameters[parameter_offset:]}",
                RuntimeWarning,
            )

    def get_command_description(self) -> str:
        return f"{self.COMMAND_CLASS}-{self.COMMAND_NAME} ({self.NAME})"

    @override
    def __str__(self) -> str:
        str_repr = f"{self.get_command_description()}: {{ "
        for parameter_def in self.PARAMETER_DEFS:
            parameter_name, __fmt = self.__get_name_and_fmt_from_def(parameter_def)
            parameter_value = getattr(self, parameter_name)
            str_repr += f"{parameter_name}={parameter_value} ({hex(parameter_value)}), "
        str_repr = str_repr[:-2] + " }"

        return str_repr

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, self.__class__):
            return self.raw_parameters == value.raw_parameters
        else:
            return False

    @override
    def __ne__(self, value: object, /) -> bool:
        return not self.__eq__(value)

    def __bytes__(self) -> bytes:
        b = b"\x1b" + self.get_command_header()
        for parameter_def in self.PARAMETER_DEFS:
            parameter_name, fmt = self.__get_name_and_fmt_from_def(parameter_def)
            b += struct.pack(fmt, getattr(self, parameter_name))
        return b


class EscprCommandUnknown:
    def __init__(self, header: bytes, params: bytes):
        self.header: bytes = header
        self.raw_parameters: bytes = params
        self.parameters: dict[str, int] = {}

    def get_command_header(self) -> bytes:
        return self.header

    def get_command_description(self) -> str:
        return f"{self.get_command_header()} ({'Unknown'})"

    @override
    def __str__(self) -> str:
        return f"UnknownCommand ({self.header}): {self.raw_parameters}"

    @override
    def __eq__(self, value: object, /) -> bool:
        if isinstance(value, self.__class__):
            return (
                self.raw_parameters == value.raw_parameters
                and self.header == value.header
            )
        else:
            return False

    @override
    def __ne__(self, value: object, /) -> bool:
        return not self.__eq__(value)


class EscprCommandJSetj(EscprCommand):
    NAME: str = "JobStart"
    COMMAND_CLASS: str = "j"
    PARAMETER_LENGTH: int = 22
    COMMAND_NAME: str = "setj"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        ("PaperWidth", ">I"),
        ("PaperLength", ">I"),
        ("TopMargin", ">h"),
        ("LeftMargin", ">h"),
        ("PrintableAreaWidth", ">I"),
        ("PrintableAreaLength", ">I"),
        "InResolution",
        "PrintDirection",
    ]


class EscprCommandMSetc(EscprCommand):
    NAME: str = "CustomPrintSetting"
    COMMAND_CLASS: str = "m"
    PARAMETER_LENGTH: int = 1
    COMMAND_NAME: str = "setc"

    PARAMETER_DEFS: list[str | tuple[str, str]] = ["MediaSizeID"]


class EscprCommandMSeti(EscprCommand):
    NAME: str = "MechaAdditionalInfo"
    COMMAND_CLASS: str = "m"
    PARAMETER_LENGTH: int = 4
    COMMAND_NAME: str = "seti"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        "SingleBkPrintModePermission",
        ("PrintDensityForRubbingReductionPriority", ">H"),
        "BottomEdgePrintQualityPriority",
    ]


class EscprCommandMSetiShort(EscprCommand):
    NAME: str = "MechaAdditionalInfoShort"
    COMMAND_CLASS: str = "m"
    PARAMETER_LENGTH: int = 1
    COMMAND_NAME: str = "seti"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        "SingleBkPrintModePermission?",
    ]


class EscprCommandMSetm(EscprCommand):
    NAME: str = "MechaSetting"
    COMMAND_CLASS: str = "m"
    PARAMETER_LENGTH: int = 7
    COMMAND_NAME: str = "setm"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        "MediaSizeID",
        "BorderlessMode",
        "SkipBlankPage",
        "DocumentType",
        "BkPrintMode",
        "BkInkSaveMode",
        "CrossDirectionMode",
    ]


class EscprCommandPSeti(EscprCommand):
    NAME: str = "PageImageProcessing"
    COMMAND_CLASS: str = "p"
    PARAMETER_LENGTH: int = 5
    COMMAND_NAME: str = "seti"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        ("MaxBottomY", ">I"),
        "IDCardData",
    ]


class EscprCommandPSetn(EscprCommand):
    NAME: str = "PageNum"
    COMMAND_CLASS: str = "p"
    PARAMETER_LENGTH: int = 1
    COMMAND_NAME: str = "setn"

    PARAMETER_DEFS: list[str | tuple[str, str]] = ["NextPage"]


class EscprCommandPSetq(EscprCommand):
    NAME: str = "PageQuality"
    COMMAND_CLASS: str = "p"
    PARAMETER_LENGTH: int = 12
    COMMAND_NAME: str = "setq"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        "ColorMono",
        "ColorPlane",
        "LUT",
        ("GammaCorrect", ">H"),
        "PrintDuty",
        "Brightness",
        "Contrast",
        "Saturation",
        "R_Adjustment",
        "G_Adjustment",
        "B_Adjustment",
    ]


class EscprCommandPSttp(EscprCommand):
    NAME: str = "PageStart"
    COMMAND_CLASS: str = "p"
    PARAMETER_LENGTH: int = 0
    COMMAND_NAME: str = "sttp"

    PARAMETER_DEFS: list[str | tuple[str, str]] = []


class EscprCommandQSetb(EscprCommand):
    NAME: str = "ABWPSetting"
    COMMAND_CLASS: str = "q"
    PARAMETER_LENGTH: int = 36
    COMMAND_NAME: str = "setb"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        ("CircleX", ">I"),
        ("CircleY", ">I"),
        ("MonoGamma", ">I"),
        ("MonoBrightness", ">I"),
        ("ShadowTonality", ">I"),
        ("HighlightTonality", ">I"),
        ("MaxOpticalDensity", ">I"),
        ("HighlightPoint", ">Q"),
    ]


class EscprCommandQSeti(EscprCommand):
    NAME: str = "ImageProcessing"
    COMMAND_CLASS: str = "q"
    PARAMETER_LENGTH: int = 10
    COMMAND_NAME: str = "seti"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        "CompressMode",
        "StaticAPFSetting",
        "ConvertColorSpaceSetting",
        "BarcodeMode",
        "FaceOrder",
        "StandardFastMode",
        "OverCoatSetting",
        "GlossPrioritySetting",
        "HostAPFSetting",
        "BindingPosition",
    ]


class EscprCommandQSetl(EscprCommand):
    NAME: str = "UserMediaIDSetting"
    COMMAND_CLASS: str = "q"
    PARAMETER_LENGTH: int = 4
    COMMAND_NAME: str = "setl"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [("UserMediaTypeID", ">I")]


class EscprCommandQSetq(EscprCommand):
    NAME: str = "PrintQuality"
    COMMAND_CLASS: str = "q"
    PARAMETER_LENGTH: int = 9
    COMMAND_NAME: str = "setq"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        "MediaTypeID",
        "PrintQuality",
        "ColorMono",
        "Brightness",
        "Contrast",
        "Saturation",
        "ColorPlane",
        ("PaletteSize", ">H"),
    ]


class EscprCommandUChku(EscprCommand):
    NAME: str = "CheckPrintSetting"
    COMMAND_CLASS: str = "u"
    PARAMETER_LENGTH: int = 2
    COMMAND_NAME: str = "chku"

    PARAMETER_DEFS: list[str | tuple[str, str]] = [
        "NonCheckPrintMode",
        "OffsetPrintingMode",
    ]


COMMANDS: dict[bytes, type[EscprCommand]] = {
    EscprCommandJSetj.get_command_header(): EscprCommandJSetj,
    EscprCommandMSetc.get_command_header(): EscprCommandMSetc,
    EscprCommandMSeti.get_command_header(): EscprCommandMSeti,
    EscprCommandMSetiShort.get_command_header(): EscprCommandMSetiShort,
    EscprCommandMSetm.get_command_header(): EscprCommandMSetm,
    EscprCommandPSeti.get_command_header(): EscprCommandPSeti,
    EscprCommandPSetn.get_command_header(): EscprCommandPSetn,
    EscprCommandPSetq.get_command_header(): EscprCommandPSetq,
    EscprCommandPSttp.get_command_header(): EscprCommandPSttp,
    EscprCommandQSetb.get_command_header(): EscprCommandQSetb,
    EscprCommandQSeti.get_command_header(): EscprCommandQSeti,
    EscprCommandQSetl.get_command_header(): EscprCommandQSetl,
    EscprCommandQSetq.get_command_header(): EscprCommandQSetq,
    EscprCommandUChku.get_command_header(): EscprCommandUChku,
}
