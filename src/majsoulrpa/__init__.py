from logging import NullHandler, getLogger

from ._rpa import RPA
from ._version import __version__

getLogger(__name__).addHandler(NullHandler())

__all__ = [
    "__version__",
    "RPA",
]
