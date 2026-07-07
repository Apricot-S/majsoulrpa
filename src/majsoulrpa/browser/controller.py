import base64
import binascii
from random import Random

from majsoulrpa.browser.messages import (
    BrowserErrorResponse,
    BrowserResponse,
    ClickCommand,
    ClickResponse,
    MoveMouseCommand,
    MoveMouseResponse,
    PressKeyCommand,
    PressKeyResponse,
    ScreenshotCommand,
    ScreenshotResponse,
    TextInputCommand,
    TextInputResponse,
)
from majsoulrpa.browser.transport import BrowserClientTransport
from majsoulrpa.timing import get_random_delay

DEFAULT_CLICK_MOUSE_DOWN_UP_DELAY_SECONDS = 0.1
DEFAULT_TEXT_INPUT_CHARACTER_DELAY_SECONDS = 0.05
DEFAULT_KEY_DOWN_UP_DELAY_SECONDS = 0.05


class BrowserOperationError(RuntimeError):
    pass


class RemoteBrowserController:
    def __init__(
        self,
        transport: BrowserClientTransport,
        *,
        rng: Random | None = None,
        click_mouse_down_up_delay_seconds: float = (
            DEFAULT_CLICK_MOUSE_DOWN_UP_DELAY_SECONDS
        ),
        text_input_character_delay_seconds: float = (
            DEFAULT_TEXT_INPUT_CHARACTER_DELAY_SECONDS
        ),
        key_down_up_delay_seconds: float = DEFAULT_KEY_DOWN_UP_DELAY_SECONDS,
    ) -> None:
        self._transport = transport
        self._rng = rng
        self._click_mouse_down_up_delay_seconds = (
            click_mouse_down_up_delay_seconds
        )
        self._text_input_character_delay_seconds = (
            text_input_character_delay_seconds
        )
        self._key_down_up_delay_seconds = key_down_up_delay_seconds

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

    async def move_mouse(self, x: float, y: float) -> MoveMouseResponse:
        return await self._request_move_mouse(MoveMouseCommand(x=x, y=y))

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

    async def press_key(self, key: str) -> PressKeyResponse:
        return await self._request_press_key(
            PressKeyCommand(
                key=key,
                key_down_up_delay_seconds=get_random_delay(
                    self._key_down_up_delay_seconds,
                    rng=self._rng,
                ),
            ),
        )

    async def screenshot(self) -> bytes:
        response = await self._request_screenshot(ScreenshotCommand())
        try:
            return base64.b64decode(response.screenshot_base64, validate=True)
        except binascii.Error as error:
            msg = "screenshot response is not valid base64."
            raise BrowserOperationError(msg) from error

    async def _request_click(self, command: ClickCommand) -> ClickResponse:
        await self._transport.send_command(command)
        response = await self._transport.recv_response()
        if isinstance(response, ClickResponse):
            return response
        raise self._response_error(response)

    async def _request_move_mouse(
        self,
        command: MoveMouseCommand,
    ) -> MoveMouseResponse:
        await self._transport.send_command(command)
        response = await self._transport.recv_response()
        if isinstance(response, MoveMouseResponse):
            return response
        raise self._response_error(response)

    async def _request_text_input(
        self,
        command: TextInputCommand,
    ) -> TextInputResponse:
        await self._transport.send_command(command)
        response = await self._transport.recv_response()
        if isinstance(response, TextInputResponse):
            return response
        raise self._response_error(response)

    async def _request_press_key(
        self,
        command: PressKeyCommand,
    ) -> PressKeyResponse:
        await self._transport.send_command(command)
        response = await self._transport.recv_response()
        if isinstance(response, PressKeyResponse):
            return response
        raise self._response_error(response)

    async def _request_screenshot(
        self,
        command: ScreenshotCommand,
    ) -> ScreenshotResponse:
        await self._transport.send_command(command)
        response = await self._transport.recv_response()
        if isinstance(response, ScreenshotResponse):
            return response
        raise self._response_error(response)

    @staticmethod
    def _response_error(response: BrowserResponse) -> BrowserOperationError:
        if isinstance(response, BrowserErrorResponse):
            return BrowserOperationError(response.message)
        msg = f"unexpected browser response: {response.type}"
        return BrowserOperationError(msg)
