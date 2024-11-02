"""An RPA framework for Mahjong Soul."""

from logging import NullHandler, getLogger

from ._version import __version__

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    # submodules
    "client",  # type: ignore[reportUnsupportedDunderAll]
    "config",  # type: ignore[reportUnsupportedDunderAll]
    "presentation",  # type: ignore[reportUnsupportedDunderAll]
    "yostar_login",  # type: ignore[reportUnsupportedDunderAll]
    "player",  # type: ignore[reportUnsupportedDunderAll]
    "timeout",  # type: ignore[reportUnsupportedDunderAll]
    # Non-modules
    "__version__",
]
