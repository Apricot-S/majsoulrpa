from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_CREATE_IMAGE = FileImage(_PARENT / "create.png")
_CREATE_CONFIG = Config.from_file(_PARENT / "create.toml")
CREATE = Matcher(_CREATE_IMAGE, _CREATE_CONFIG)

_UNSELECTED_IMAGE = FileImage(_PARENT / "unselected.png")

_FOUR_PLAYER_CONFIG = Config.from_file(_PARENT / "4-player.toml")
FOUR_PLAYER = Matcher(_UNSELECTED_IMAGE, _FOUR_PLAYER_CONFIG)

__all__ = [
    "CREATE",
]
