from logging import NullHandler, getLogger

from majsoulrpa._version import __version__
from majsoulrpa.config_input import ConfigInput
from majsoulrpa.rpa_client import RPAClient

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "ConfigInput",
    "RPAClient",
    "__version__",
]

# submodules
__all__ += [
    "exceptions",  # type: ignore[reportUnsupportedDunderAll]
    "presentation",  # type: ignore[reportUnsupportedDunderAll]
]
