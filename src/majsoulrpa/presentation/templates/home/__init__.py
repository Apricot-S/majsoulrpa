from pathlib import Path

from majsoulrpa.presentation.template import Config, FileImage, Matcher

_PARENT = Path(__file__).parent

_SUMMON_IMAGE = FileImage(_PARENT / "summon.png")
_SUMMON_CONFIG = Config.from_file(_PARENT / "summon.toml")
SUMMON = Matcher(_SUMMON_IMAGE, _SUMMON_CONFIG)
