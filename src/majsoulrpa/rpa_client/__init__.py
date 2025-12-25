from typing import TYPE_CHECKING

from majsoulrpa.rpa_client.config import Config

if TYPE_CHECKING:
    from majsoulrpa.rpa_client.core import RPAClient
else:
    try:
        from majsoulrpa.rpa_client.core import RPAClient
    except ModuleNotFoundError:

        class RPAClient:
            def __init__(self, *args, **kwargs) -> None:  # noqa: ARG002
                msg = "`RPAClient` requires `client` extra"
                raise RuntimeError(msg)


__all__ = [
    "Config",
    "RPAClient",
]
