from typing import TYPE_CHECKING

from majsoulrpa.rpa_client.config import Config

if TYPE_CHECKING:
    from majsoulrpa.rpa_client.core import RPAClient
else:
    try:
        from majsoulrpa.rpa_client.core import RPAClient
    except ModuleNotFoundError:

        class _RPAClientUnavailable:
            def __init__(self, *args, **kwargs) -> None:  # noqa: ARG002
                msg = "`RPAClient` requires `client` extra"
                raise RuntimeError(msg)

        RPAClient = _RPAClientUnavailable  # type: ignore[assignment,misc]

__all__ = [
    "Config",
    "RPAClient",
]
