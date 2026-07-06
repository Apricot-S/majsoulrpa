import importlib
from typing import TYPE_CHECKING, Any

from majsoulrpa.browser.controller import (
    BrowserOperationError,
    RemoteBrowserController,
)
from majsoulrpa.browser.host import BrowserBackend, BrowserHost
from majsoulrpa.browser.json_stream import (
    BrowserJsonStreamTransport,
    parse_browser_command_json,
    parse_browser_response_json,
)
from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserErrorResponse,
    BrowserResponse,
    ClickCommand,
    ClickResponse,
    ScreenshotCommand,
    ScreenshotResponse,
    TextInputCommand,
    TextInputResponse,
)
from majsoulrpa.browser.server import (
    BrowserCommandExecutor,
    BrowserRequestHandler,
    BrowserRequestTransport,
)
from majsoulrpa.browser.tcp import BrowserTcpAddress, BrowserTcpServer
from majsoulrpa.browser.transport import BrowserTransport
from majsoulrpa.browser.zmq import (
    BrowserZmqClientTransport,
    BrowserZmqServerTransport,
)

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
    "BrowserBackend",
    "BrowserCommand",
    "BrowserCommandExecutor",
    "BrowserErrorResponse",
    "BrowserHost",
    "BrowserJsonStreamTransport",
    "BrowserOperationError",
    "BrowserRequestHandler",
    "BrowserRequestTransport",
    "BrowserResponse",
    "BrowserTcpAddress",
    "BrowserTcpServer",
    "BrowserTransport",
    "BrowserZmqClientTransport",
    "BrowserZmqServerTransport",
    "ClickCommand",
    "ClickResponse",
    "PlaywrightBrowserBackend",
    "PlaywrightCommandExecutor",
    "RemoteBrowserController",
    "ScreenshotCommand",
    "ScreenshotResponse",
    "TextInputCommand",
    "TextInputResponse",
    "parse_browser_command_json",
    "parse_browser_response_json",
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
