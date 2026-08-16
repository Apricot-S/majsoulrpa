from logging import NullHandler, getLogger

from majsoulrpa.app import RPAApp
from majsoulrpa.config import AppConfig

getLogger(__name__).addHandler(NullHandler())

__version__ = "0.1.0.dev5"

__all__ = ["AppConfig", "RPAApp", "__version__"]
