import argparse
from enum import Enum
from pathlib import Path
import tomlkit


class PrintMode(Enum):
    Auto = 1
    CmOff = 2
    ABW = 3


class Config:
    def __init__(self, config_path: Path, create: bool = True) -> None:
        self.config_path: Path = config_path
        if not self.config_path.exists() and create:
            self.config_path.touch()
        with open(self.config_path) as cf:
            self.__inner: tomlkit.TOMLDocument = tomlkit.load(cf)

    def set_print_mode(self, print_mode: PrintMode):
        self.__inner["print_mode"] = print_mode.name

    def get_print_mode(self) -> PrintMode:
        return PrintMode[self.__inner.get("print_mode", "Auto")]

    def save_config(self):
        with open(self.config_path, "w") as cf:
            tomlkit.dump(self.__inner, cf)


def set_config_cli():
    parser = argparse.ArgumentParser(
        prog="escpr2-proxy-config",
        description="Set escpr2-proxy config options",
    )
    parser.add_argument("config_path")
    parser.add_argument(
        "print_mode", choices=[print_mode.name for print_mode in PrintMode]
    )
    args = parser.parse_args()

    config = Config(Path(args.config_path))
    old_mode = config.get_print_mode()
    config.set_print_mode(PrintMode[args.print_mode])
    config.save_config()
    print(f"Set mode from {old_mode} to {args.print_mode}")
