# ruff: noqa: F401
from logging import NullHandler, getLogger

from ._rpa import RPA
from ._version import __version__

getLogger(__name__).addHandler(NullHandler())
