from majsoulrpa.browser.messages import (
    BrowserErrorResponse,
    BrowserResponse,
    ClickCommand,
    ClickResponse,
    ScreenshotCommand,
    ScreenshotResponse,
    TextInputCommand,
    TextInputResponse,
)
from majsoulrpa.browser.transport import BrowserTransport


class BrowserOperationError(RuntimeError):
    pass


class RemoteBrowserController:
    def __init__(self, transport: BrowserTransport) -> None:
        self._transport = transport

    async def click(self, x: float, y: float) -> ClickResponse:
        return await self._request_click(ClickCommand(x=x, y=y))

    async def input_text(self, text: str) -> TextInputResponse:
        return await self._request_text_input(TextInputCommand(text=text))

    async def take_screenshot(self) -> ScreenshotResponse:
        return await self._request_screenshot(ScreenshotCommand())

    async def _request_click(self, command: ClickCommand) -> ClickResponse:
        await self._transport.send(command)
        response = await self._transport.recv()
        if isinstance(response, ClickResponse):
            return response
        raise self._response_error(response)

    async def _request_text_input(
        self,
        command: TextInputCommand,
    ) -> TextInputResponse:
        await self._transport.send(command)
        response = await self._transport.recv()
        if isinstance(response, TextInputResponse):
            return response
        raise self._response_error(response)

    async def _request_screenshot(
        self,
        command: ScreenshotCommand,
    ) -> ScreenshotResponse:
        await self._transport.send(command)
        response = await self._transport.recv()
        if isinstance(response, ScreenshotResponse):
            return response
        raise self._response_error(response)

    @staticmethod
    def _response_error(response: BrowserResponse) -> BrowserOperationError:
        if isinstance(response, BrowserErrorResponse):
            return BrowserOperationError(response.message)
        msg = f"unexpected browser response: {response.type}"
        return BrowserOperationError(msg)
