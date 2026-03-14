from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_LOGIN_1_IMAGE = FileImage(_PARENT / "login_1.png")
_LOGIN_1_CONFIG = Config.from_file(_PARENT / "login_1.toml")
LOGIN_1 = Matcher(_LOGIN_1_IMAGE, _LOGIN_1_CONFIG)

_SEND_IMAGE = FileImage(_PARENT / "send.png")
_SEND_CONFIG = Config.from_file(_PARENT / "send.toml")
SEND = Matcher(_SEND_IMAGE, _SEND_CONFIG)

_CONFIRM_IMAGE = FileImage(_PARENT / "confirm.png")
_CONFIRM_CONFIG = Config.from_file(_PARENT / "confirm.toml")
CONFIRM = Matcher(_CONFIRM_IMAGE, _CONFIRM_CONFIG)

_LOGIN_2_IMAGE = FileImage(_PARENT / "login_2.png")
_LOGIN_2_CONFIG = Config.from_file(_PARENT / "login_2.toml")
LOGIN_2 = Matcher(_LOGIN_2_IMAGE, _LOGIN_2_CONFIG)

_OK_IMAGE = FileImage(_PARENT / "ok.png")
_OK_CONFIG = Config.from_file(_PARENT / "ok.toml")
OK = Matcher(_OK_IMAGE, _OK_CONFIG)

__all__ = [
    "CONFIRM",
    "LOGIN_1",
    "LOGIN_2",
    "OK",
    "SEND",
]
