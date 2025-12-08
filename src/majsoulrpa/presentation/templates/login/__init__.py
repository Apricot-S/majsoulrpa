from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_LOGIN_1_IMAGE = FileImage(_PARENT / "login_1.png")
_LOGIN_1_CONFIG = Config.from_file(_PARENT / "login_1.toml")
LOGIN_1 = Matcher(_LOGIN_1_IMAGE, _LOGIN_1_CONFIG)

_UNAVAILABLE_IMAGE = FileImage(_PARENT / "unavailable.png")
_UNAVAILABLE_CONFIG = Config.from_file(_PARENT / "unavailable.toml")
UNAVAILABLE = Matcher(_UNAVAILABLE_IMAGE, _UNAVAILABLE_CONFIG)

_CONFIRM_IMAGE = FileImage(_PARENT / "confirm.png")
_CONFIRM_CONFIG = Config.from_file(_PARENT / "confirm.toml")
CONFIRM = Matcher(_CONFIRM_IMAGE, _CONFIRM_CONFIG)

_LOGIN_2_IMAGE = FileImage(_PARENT / "login_2.png")
_LOGIN_2_CONFIG = Config.from_file(_PARENT / "login_2.toml")
LOGIN_2 = Matcher(_LOGIN_2_IMAGE, _LOGIN_2_CONFIG)
