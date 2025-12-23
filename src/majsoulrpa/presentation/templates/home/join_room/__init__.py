from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_CONFIRM_IMAGE = FileImage(_PARENT / "confirm.png")
_CONFIRM_CONFIG = Config.from_file(_PARENT / "confirm.toml")
CONFIRM = Matcher(_CONFIRM_IMAGE, _CONFIRM_CONFIG)

__all__ = [
    "CONFIRM",
]
