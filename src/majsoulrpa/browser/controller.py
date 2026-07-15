import base64
import binascii
from random import Random

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
from majsoulrpa.browser.transport import BrowserClientTransport
from majsoulrpa.timing import get_random_delay

DEFAULT_CLICK_HOVER_DELAY_SECONDS = 0.12
DEFAULT_CLICK_MOUSE_DOWN_UP_DELAY_SECONDS = 0.1
DEFAULT_TEXT_INPUT_CHARACTER_DELAY_SECONDS = 0.05
DEFAULT_KEY_DOWN_UP_DELAY_SECONDS = 0.1
DEFAULT_YOSTAR_AUTH_TIMEOUT_SECONDS = 1.0


class BrowserOperationError(RuntimeError):
    pass


class RemoteBrowserController:
    def __init__(
        self,
        transport: BrowserClientTransport,
        *,
        rng: Random | None = None,
        click_hover_delay_seconds: float = DEFAULT_CLICK_HOVER_DELAY_SECONDS,
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
        self._click_hover_delay_seconds = click_hover_delay_seconds
        self._click_mouse_down_up_delay_seconds = (
            click_mouse_down_up_delay_seconds
        )
        self._text_input_character_delay_seconds = (
            text_input_character_delay_seconds
        )
        self._key_down_up_delay_seconds = key_down_up_delay_seconds

    async def click(
        self,
        x: float,
        y: float,
        *,
        warp: bool = False,
    ) -> ClickResponse:
        return await self._request(
            ClickCommand(
                x=x,
                y=y,
                hover_delay_seconds=(
                    None if warp else self._click_hover_delay_seconds
                ),
                mouse_down_up_delay_seconds=get_random_delay(
                    self._click_mouse_down_up_delay_seconds,
                    rng=self._rng,
                ),
            ),
            ClickResponse,
        )

    async def move_mouse(self, x: float, y: float) -> MoveMouseResponse:
        return await self._request(
            MoveMouseCommand(x=x, y=y),
            MoveMouseResponse,
        )

    async def input_text(self, text: str) -> TextInputResponse:
        return await self._request(
            TextInputCommand(
                text=text,
                character_delay_seconds=get_random_delay(
                    self._text_input_character_delay_seconds,
                    rng=self._rng,
                ),
            ),
            TextInputResponse,
        )

    async def press_key(self, key: str) -> PressKeyResponse:
        return await self._request(
            PressKeyCommand(
                key=key,
                key_down_up_delay_seconds=get_random_delay(
                    self._key_down_up_delay_seconds,
                    rng=self._rng,
                ),
            ),
            PressKeyResponse,
        )

    async def screenshot(self) -> bytes:
        response = await self._request(ScreenshotCommand(), ScreenshotResponse)
        try:
            return base64.b64decode(response.screenshot_base64, validate=True)
        except binascii.Error as error:
            msg = "screenshot response is not valid base64."
            raise BrowserOperationError(msg) from error

    async def goto_url(self, url: str) -> GotoUrlResponse:
        return await self._request(GotoUrlCommand(url=url), GotoUrlResponse)

    async def reload(self) -> ReloadResponse:
        return await self._request(ReloadCommand(), ReloadResponse)

    async def stop_browser_host(self) -> StopBrowserHostResponse:
        return await self._request(
            StopBrowserHostCommand(),
            StopBrowserHostResponse,
        )

    async def click_and_wait_for_yostar_auth(
        self,
        x: float,
        y: float,
    ) -> YostarAuthAcceptedResponse | YostarAuthRejectedResponse:
        return await self._request(
            ClickAndWaitForYostarAuthCommand(
                x=x,
                y=y,
                mouse_down_up_delay_seconds=get_random_delay(
                    self._click_mouse_down_up_delay_seconds,
                    rng=self._rng,
                ),
                timeout_seconds=DEFAULT_YOSTAR_AUTH_TIMEOUT_SECONDS,
            ),
            (YostarAuthAcceptedResponse, YostarAuthRejectedResponse),
        )

    async def _request[ResponseT: BrowserResponse](
        self,
        command: BrowserCommand,
        response_type: type[ResponseT] | tuple[type[ResponseT], ...],
    ) -> ResponseT:
        await self._transport.send_command(command)
        response = await self._transport.recv_response()
        if isinstance(response, response_type):
            return response
        raise self._response_error(response)

    @staticmethod
    def _response_error(response: BrowserResponse) -> BrowserOperationError:
        if isinstance(response, BrowserErrorResponse):
            return BrowserOperationError(response.message)
        msg = f"unexpected browser response: {response.type}"
        return BrowserOperationError(msg)
