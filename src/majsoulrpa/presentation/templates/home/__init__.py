from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_SUMMON_IMAGE = FileImage(_PARENT / "summon.png")
_SUMMON_CONFIG = Config.from_file(_PARENT / "summon.toml")
SUMMON = Matcher(_SUMMON_IMAGE, _SUMMON_CONFIG)

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
