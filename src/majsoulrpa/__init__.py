"""Provides an RPA framework for Mahjong Soul."""

from logging import NullHandler, getLogger

from ._version import __version__

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "__version__",
]
