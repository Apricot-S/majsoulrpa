from logging import NullHandler, getLogger

from majsoulrpa._version import __version__
from majsoulrpa.config_input import ConfigInput

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "ConfigInput",
    "__version__",
]

# submodules
__all__ += [
    "exceptions",  # type: ignore[reportUnsupportedDunderAll]
    "presentation",  # type: ignore[reportUnsupportedDunderAll]
    "rpa_client",  # type: ignore[reportUnsupportedDunderAll]
    "yostar_login",  # type: ignore[reportUnsupportedDunderAll]
]
