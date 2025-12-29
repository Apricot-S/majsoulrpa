from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_ENTER_IMAGE = FileImage(_PARENT / "enter.png")
_ENTER_CONFIG = Config.from_file(_PARENT / "enter.toml")
ENTER = Matcher(_ENTER_IMAGE, _ENTER_CONFIG)

__all__ = [
    "ENTER",
]
