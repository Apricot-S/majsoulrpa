"""An RPA framework for Mahjong Soul."""

from logging import NullHandler, getLogger

from ._version import __version__

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "__version__",
]

# submodules
__all__ += [
    "client",  # type: ignore[reportUnsupportedDunderAll]
    "config",  # type: ignore[reportUnsupportedDunderAll]
    "player",  # type: ignore[reportUnsupportedDunderAll]
    "presentation",  # type: ignore[reportUnsupportedDunderAll]
    "timeout",  # type: ignore[reportUnsupportedDunderAll]
    "yostar_login",  # type: ignore[reportUnsupportedDunderAll]
]
