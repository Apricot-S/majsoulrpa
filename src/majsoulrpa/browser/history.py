from collections.abc import Mapping
from logging import getLogger

from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserErrorResponse,
    BrowserResponse,
    ClickAndWaitForYostarAuthCommand,
    ClickCommand,
    ClickResponse,
    GotoUrlCommand,
    GotoUrlResponse,
    MoveMouseCommand,
    MoveMouseResponse,
    PressKeyCommand,
    PressKeyResponse,
    ReloadCommand,
    ReloadResponse,
    ScreenshotCommand,
    ScreenshotResponse,
    StopBrowserHostCommand,
    StopBrowserHostResponse,
    TextInputCommand,
    TextInputResponse,
    YostarAuthAcceptedResponse,
    YostarAuthRejectedResponse,
)
from majsoulrpa.browser.server import BrowserCommandExecutor
from majsoulrpa.browser.transport import BrowserClientTransport

_client_logger = getLogger("majsoulrpa.browser.client")
_host_logger = getLogger("majsoulrpa.browser.host")


class LoggingBrowserClientTransport:
    def __init__(self, transport: BrowserClientTransport) -> None:
        self._transport = transport

    async def send_command(self, command: BrowserCommand) -> None:
        _client_logger.debug(
            "browser client command: %s",
            summarize_browser_command(command),
        )
        await self._transport.send_command(command)

    async def recv_response(self) -> BrowserResponse:
        response = await self._transport.recv_response()
        _client_logger.debug(
            "browser client response: %s",
            summarize_browser_response(response),
        )
        return response


class LoggingBrowserCommandExecutor:
    def __init__(self, executor: BrowserCommandExecutor) -> None:
        self._executor = executor

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        _host_logger.debug(
            "browser host command: %s",
            summarize_browser_command(command),
        )
        response = await self._executor.execute(command)
        _host_logger.debug(
            "browser host response: %s",
            summarize_browser_response(response),
        )
        return response


def summarize_browser_command(command: BrowserCommand) -> Mapping[str, object]:
    match command:
        case ClickCommand():
            return {
                "type": command.type,
                "x": command.x,
                "y": command.y,
                "mouse_down_up_delay_seconds": (
                    command.mouse_down_up_delay_seconds
                ),
            }
        case MoveMouseCommand():
            return {
                "type": command.type,
                "x": command.x,
                "y": command.y,
            }
        case TextInputCommand():
            return {
                "type": command.type,
                "text_length": len(command.text),
                "character_delay_seconds": (command.character_delay_seconds),
            }
        case PressKeyCommand():
            return {
                "type": command.type,
                "key": command.key,
                "key_down_up_delay_seconds": (
                    command.key_down_up_delay_seconds
                ),
            }
        case ScreenshotCommand():
            return {"type": command.type}
        case GotoUrlCommand():
            return {
                "type": command.type,
                "url": command.url,
            }
        case ReloadCommand():
            return {"type": command.type}
        case StopBrowserHostCommand():
            return {"type": command.type}
        case ClickAndWaitForYostarAuthCommand():
            return {
                "type": command.type,
                "x": command.x,
                "y": command.y,
                "mouse_down_up_delay_seconds": (
                    command.mouse_down_up_delay_seconds
                ),
                "timeout_seconds": command.timeout_seconds,
            }


def summarize_browser_response(
    response: BrowserResponse,
) -> Mapping[str, object]:
    match response:
        case ClickResponse():
            return {
                "type": response.type,
                "x": response.x,
                "y": response.y,
            }
        case MoveMouseResponse():
            return {
                "type": response.type,
                "x": response.x,
                "y": response.y,
            }
        case TextInputResponse():
            return {
                "type": response.type,
                "text_length": len(response.text),
            }
        case PressKeyResponse():
            return {
                "type": response.type,
                "key": response.key,
            }
        case ScreenshotResponse():
            return {
                "type": response.type,
                "screenshot_base64_length": len(response.screenshot_base64),
            }
        case GotoUrlResponse():
            return {
                "type": response.type,
                "url": response.url,
            }
        case ReloadResponse():
            return {"type": response.type}
        case StopBrowserHostResponse():
            return {"type": response.type}
        case YostarAuthAcceptedResponse():
            return {"type": response.type}
        case YostarAuthRejectedResponse():
            return {
                "type": response.type,
                "application_code": response.application_code,
            }
        case BrowserErrorResponse():
            return {
                "type": response.type,
                "message_length": len(response.message),
            }
