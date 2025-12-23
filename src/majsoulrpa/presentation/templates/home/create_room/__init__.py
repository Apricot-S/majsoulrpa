from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_CREATE_IMAGE = FileImage(_PARENT / "create.png")
_CREATE_CONFIG = Config.from_file(_PARENT / "create.toml")
CREATE = Matcher(_CREATE_IMAGE, _CREATE_CONFIG)

_UNSELECTED_IMAGE = FileImage(_PARENT / "unselected.png")

_FOUR_PLAYER_CONFIG = Config.from_file(_PARENT / "4-player.toml")
FOUR_PLAYER = Matcher(_UNSELECTED_IMAGE, _FOUR_PLAYER_CONFIG)

_THREE_PLAYER_CONFIG = Config.from_file(_PARENT / "3-player.toml")
THREE_PLAYER = Matcher(_UNSELECTED_IMAGE, _THREE_PLAYER_CONFIG)

_ONE_GAME_CONFIG = Config.from_file(_PARENT / "1_game.toml")
ONE_GAME = Matcher(_UNSELECTED_IMAGE, _ONE_GAME_CONFIG)

_EAST_ONLY_CONFIG = Config.from_file(_PARENT / "east_only.toml")
EAST_ONLY = Matcher(_UNSELECTED_IMAGE, _EAST_ONLY_CONFIG)

_TWO_WIND_MATCH_CONFIG = Config.from_file(_PARENT / "two-wind_match.toml")
TWO_WIND_MATCH = Matcher(_UNSELECTED_IMAGE, _TWO_WIND_MATCH_CONFIG)

_VS_AI_CONFIG = Config.from_file(_PARENT / "vs_ai.toml")
VS_AI = Matcher(_UNSELECTED_IMAGE, _VS_AI_CONFIG)

_FIVE_PLUS_TEN_CONFIG = Config.from_file(_PARENT / "5+10s.toml")
FIVE_PLUS_TEN = Matcher(_UNSELECTED_IMAGE, _FIVE_PLUS_TEN_CONFIG)

_FIVE_PLUS_TWENTY_CONFIG = Config.from_file(_PARENT / "5+20s.toml")
FIVE_PLUS_TWENTY = Matcher(_UNSELECTED_IMAGE, _FIVE_PLUS_TWENTY_CONFIG)

__all__ = [
    "CREATE",
    "EAST_ONLY",
    "FIVE_PLUS_TEN",
    "FIVE_PLUS_TWENTY",
    "FOUR_PLAYER",
    "ONE_GAME",
    "THREE_PLAYER",
    "TWO_WIND_MATCH",
    "VS_AI",
]
