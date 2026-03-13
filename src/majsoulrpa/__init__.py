from logging import NullHandler, getLogger

from majsoulrpa.config_input import ConfigInput

getLogger(__name__).addHandler(NullHandler())

__version__ = "0.1.0"

__all__ = [
    "ConfigInput",
    "__version__",
]

# submodules
__all__ += [
    "exceptions",
    "presentation",
    "rpa_client",
    "yostar_login",
]
