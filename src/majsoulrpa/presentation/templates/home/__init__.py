from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher
from majsoulrpa.presentation.templates.home import create_room, join_room

_PARENT = Path(__file__).parent

_SUMMON_IMAGE = FileImage(_PARENT / "summon.png")
_SUMMON_CONFIG = Config.from_file(_PARENT / "summon.toml")
SUMMON = Matcher(_SUMMON_IMAGE, _SUMMON_CONFIG)

_JADE_IMAGE = FileImage(_PARENT / "jade.png")
_JADE_CONFIG = Config.from_file(_PARENT / "jade.toml")
JADE = Matcher(_JADE_IMAGE, _JADE_CONFIG)

_NOTIFICATION_CLOSE_IMAGE = FileImage(_PARENT / "notification_close.png")
_NOTIFICATION_CLOSE_CONFIG = Config.from_file(
    _PARENT / "notification_close.toml",
)
NOTIFICATION_CLOSE = Matcher(
    _NOTIFICATION_CLOSE_IMAGE,
    _NOTIFICATION_CLOSE_CONFIG,
)

_MAIL_CLOSE_IMAGE = FileImage(_PARENT / "mail_close.png")
_MAIL_CLOSE_CONFIG = Config.from_file(_PARENT / "mail_close.toml")
MAIL_CLOSE = Matcher(_MAIL_CLOSE_IMAGE, _MAIL_CLOSE_CONFIG)

_EVENT_CLOSE_IMAGE = FileImage(_PARENT / "event_close.png")
_EVENT_CLOSE_CONFIG = Config.from_file(_PARENT / "event_close.toml")
EVENT_CLOSE = Matcher(_EVENT_CLOSE_IMAGE, _EVENT_CLOSE_CONFIG)

_REWARDS_SIGN_IN_IMAGE = FileImage(_PARENT / "rewards_sign_in.png")
_REWARDS_SIGN_IN_CONFIG = Config.from_file(_PARENT / "rewards_sign_in.toml")
REWARDS_SIGN_IN = Matcher(_REWARDS_SIGN_IN_IMAGE, _REWARDS_SIGN_IN_CONFIG)

_REWARDS_CONFIRM_IMAGE = FileImage(_PARENT / "rewards_confirm.png")
_REWARDS_CONFIRM_CONFIG = Config.from_file(_PARENT / "rewards_confirm.toml")
REWARDS_CONFIRM = Matcher(_REWARDS_CONFIRM_IMAGE, _REWARDS_CONFIRM_CONFIG)

_TOURNAMENT_MATCH_IMAGE = FileImage(_PARENT / "tournament_match.png")
_TOURNAMENT_MATCH_CONFIG = Config.from_file(_PARENT / "tournament_match.toml")
TOURNAMENT_MATCH = Matcher(_TOURNAMENT_MATCH_IMAGE, _TOURNAMENT_MATCH_CONFIG)

_FRIENDLY_MATCH_IMAGE = FileImage(_PARENT / "friendly_match.png")
_FRIENDLY_MATCH_CONFIG = Config.from_file(_PARENT / "friendly_match.toml")
FRIENDLY_MATCH = Matcher(_FRIENDLY_MATCH_IMAGE, _FRIENDLY_MATCH_CONFIG)

_CREATE_ROOM_IMAGE = FileImage(_PARENT / "create_room.png")
_CREATE_ROOM_CONFIG = Config.from_file(_PARENT / "create_room.toml")
CREATE_ROOM = Matcher(_CREATE_ROOM_IMAGE, _CREATE_ROOM_CONFIG)

_JOIN_ROOM_IMAGE = FileImage(_PARENT / "join_room.png")
_JOIN_ROOM_CONFIG = Config.from_file(_PARENT / "join_room.toml")
JOIN_ROOM = Matcher(_JOIN_ROOM_IMAGE, _JOIN_ROOM_CONFIG)

__all__ = [
    "CREATE_ROOM",
    "EVENT_CLOSE",
    "FRIENDLY_MATCH",
    "JADE",
    "JOIN_ROOM",
    "MAIL_CLOSE",
    "NOTIFICATION_CLOSE",
    "REWARDS_CONFIRM",
    "REWARDS_SIGN_IN",
    "SUMMON",
    "TOURNAMENT_MATCH",
]

# submodules
__all__ += [
    "create_room",
    "join_room",
]
