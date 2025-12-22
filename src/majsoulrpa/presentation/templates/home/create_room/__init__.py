from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_CREATE_IMAGE = FileImage(_PARENT / "create.png")
_CREATE_CONFIG = Config.from_file(_PARENT / "create.toml")
CREATE = Matcher(_CREATE_IMAGE, _CREATE_CONFIG)

_UNSELECTED_IMAGE = FileImage(_PARENT / "unselected.png")

_FOUR_PLAYER_CONFIG = Config.from_file(_PARENT / "4-player.toml")
FOUR_PLAYER = Matcher(_UNSELECTED_IMAGE, _FOUR_PLAYER_CONFIG)

_TWO_WIND_MATCH_CONFIG = Config.from_file(_PARENT / "two-wind_match.toml")
TWO_WIND_MATCH = Matcher(_UNSELECTED_IMAGE, _TWO_WIND_MATCH_CONFIG)

__all__ = [
    "CREATE",
    "FOUR_PLAYER",
    "TWO_WIND_MATCH",
]
