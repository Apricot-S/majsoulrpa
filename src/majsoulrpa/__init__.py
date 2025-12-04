from majsoulrpa._version import __version__
from majsoulrpa.rpa_client import RPAClient

__all__ = [
    "RPAClient",
    "__version__",
]

# submodules
__all__ += [
    "exceptions",  # type: ignore[reportUnsupportedDunderAll]
    "presentation",  # type: ignore[reportUnsupportedDunderAll]
]
