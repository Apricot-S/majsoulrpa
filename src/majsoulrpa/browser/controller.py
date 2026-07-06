from random import Random

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
from majsoulrpa.timing import get_random_delay

DEFAULT_CLICK_MOUSE_DOWN_UP_DELAY_SECONDS = 0.1
DEFAULT_TEXT_INPUT_CHARACTER_DELAY_SECONDS = 0.05


class BrowserOperationError(RuntimeError):
    pass


class RemoteBrowserController:
    def __init__(
        self,
        transport: BrowserTransport,
        *,
        rng: Random | None = None,
        click_mouse_down_up_delay_seconds: float = (
            DEFAULT_CLICK_MOUSE_DOWN_UP_DELAY_SECONDS
        ),
        text_input_character_delay_seconds: float = (
            DEFAULT_TEXT_INPUT_CHARACTER_DELAY_SECONDS
        ),
    ) -> None:
        self._transport = transport
        self._rng = rng
        self._click_mouse_down_up_delay_seconds = (
            click_mouse_down_up_delay_seconds
        )
        self._text_input_character_delay_seconds = (
            text_input_character_delay_seconds
        )

    async def click(self, x: float, y: float) -> ClickResponse:
        return await self._request_click(
            ClickCommand(
                x=x,
                y=y,
                mouse_down_up_delay_seconds=get_random_delay(
                    self._click_mouse_down_up_delay_seconds,
                    rng=self._rng,
                ),
            ),
        )

    async def input_text(self, text: str) -> TextInputResponse:
        return await self._request_text_input(
            TextInputCommand(
                text=text,
                character_delay_seconds=get_random_delay(
                    self._text_input_character_delay_seconds,
                    rng=self._rng,
                ),
            ),
        )

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
