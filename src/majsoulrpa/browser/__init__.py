import importlib
from typing import TYPE_CHECKING, Any

from majsoulrpa.browser.controller import BrowserOperationError
from majsoulrpa.browser.runner import run_browser_host

_PLAYWRIGHT_EXPORTS = {
    "PlaywrightBrowserBackend",
    "PlaywrightCommandExecutor",
}

if TYPE_CHECKING:
    from majsoulrpa.browser.playwright import (
        PlaywrightBrowserBackend,
        PlaywrightCommandExecutor,
    )

__all__ = [
    "BrowserOperationError",
    "PlaywrightBrowserBackend",
    "PlaywrightCommandExecutor",
    "run_browser_host",
]


def __getattr__(name: str) -> Any:  # noqa: ANN401
    if name in _PLAYWRIGHT_EXPORTS:
        try:
            playwright = importlib.import_module(
                "majsoulrpa.browser.playwright",
            )
        except ModuleNotFoundError as error:
            msg = (
                f"{name} requires the 'browser' optional dependency. "
                "Install it with: pip install 'majsoulrpa[browser]'"
            )
            raise ModuleNotFoundError(msg) from error

        value = getattr(playwright, name)
        globals()[name] = value
        return value

    msg = f"module {__name__!r} has no attribute {name!r}"
    raise AttributeError(msg)


def __dir__() -> list[str]:
    return sorted({*globals(), *__all__})
