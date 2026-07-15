import asyncio
from random import Random

import pytest

from majsoulrpa.browser.controller import (
    BrowserOperationError,
    RemoteBrowserController,
)
from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserErrorResponse,
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
)


class BrowserClientTransportSpy:
    def __init__(
        self,
        *responses: (
            ClickResponse
            | GotoUrlResponse
            | MoveMouseResponse
            | PressKeyResponse
            | ReloadResponse
            | TextInputResponse
            | ScreenshotResponse
            | StopBrowserHostResponse
            | BrowserErrorResponse
            | YostarAuthAcceptedResponse
        ),
    ) -> None:
        self.sent_commands: list[BrowserCommand] = []
        self._responses = list(responses)

    async def send_command(self, command: BrowserCommand) -> None:
        self.sent_commands.append(command)

    async def recv_response(
        self,
    ) -> (
        ClickResponse
        | GotoUrlResponse
        | MoveMouseResponse
        | PressKeyResponse
        | ReloadResponse
        | TextInputResponse
        | ScreenshotResponse
        | StopBrowserHostResponse
        | BrowserErrorResponse
        | YostarAuthAcceptedResponse
    ):
        return self._responses.pop(0)


def test_remote_browser_controller_sends_click_and_text_input() -> None:
    transport = BrowserClientTransportSpy(
        ClickResponse(x=25, y=40),
        TextInputResponse(text="player@example.invalid"),
    )
    controller = RemoteBrowserController(
        transport,
        rng=Random(0),
        click_hover_delay_seconds=0.125,
    )

    asyncio.run(controller.click(25, 40))
    asyncio.run(controller.input_text("ab"))

    click_command, text_command = transport.sent_commands
    assert isinstance(click_command, ClickCommand)
    assert isinstance(text_command, TextInputCommand)
    assert click_command == ClickCommand(
        x=25,
        y=40,
        hover_delay_seconds=0.125,
        mouse_down_up_delay_seconds=click_command.mouse_down_up_delay_seconds,
    )
    assert click_command.mouse_down_up_delay_seconds > 0
    assert text_command == TextInputCommand(
        text="ab",
        character_delay_seconds=text_command.character_delay_seconds,
    )
    assert text_command.character_delay_seconds > 0


def test_remote_browser_controller_sends_warp_click_without_hover_delay() -> (
    None
):
    transport = BrowserClientTransportSpy(ClickResponse(x=25, y=40))
    controller = RemoteBrowserController(transport)

    asyncio.run(controller.click(25, 40, warp=True))

    [command] = transport.sent_commands
    assert isinstance(command, ClickCommand)
    assert command.hover_delay_seconds is None


def test_remote_browser_controller_uses_default_hover_delay() -> None:
    transport = BrowserClientTransportSpy(ClickResponse(x=25, y=40))
    controller = RemoteBrowserController(transport)

    asyncio.run(controller.click(25, 40))

    [command] = transport.sent_commands
    assert isinstance(command, ClickCommand)
    assert command.hover_delay_seconds == 0.12


def test_remote_browser_controller_clicks_and_waits_for_yostar_auth() -> None:
    transport = BrowserClientTransportSpy(YostarAuthAcceptedResponse())
    controller = RemoteBrowserController(transport, rng=Random(0))

    response = asyncio.run(controller.click_and_wait_for_yostar_auth(25, 40))

    assert response == YostarAuthAcceptedResponse()
    [command] = transport.sent_commands
    assert isinstance(command, ClickAndWaitForYostarAuthCommand)
    assert command.x == 25
    assert command.y == 40
    assert command.timeout_seconds == 1.0


def test_remote_browser_controller_sends_move_mouse() -> None:
    transport = BrowserClientTransportSpy(
        MoveMouseResponse(x=25, y=40),
    )
    controller = RemoteBrowserController(transport)

    response = asyncio.run(controller.move_mouse(25, 40))

    assert response == MoveMouseResponse(x=25, y=40)
    [command] = transport.sent_commands
    assert command == MoveMouseCommand(x=25, y=40)


def test_remote_browser_controller_sends_goto_url() -> None:
    transport = BrowserClientTransportSpy(
        GotoUrlResponse(url="https://example.invalid/path"),
    )
    controller = RemoteBrowserController(transport)

    response = asyncio.run(controller.goto_url("https://example.invalid/path"))

    assert response == GotoUrlResponse(url="https://example.invalid/path")
    assert transport.sent_commands == [
        GotoUrlCommand(url="https://example.invalid/path"),
    ]


def test_remote_browser_controller_sends_reload() -> None:
    transport = BrowserClientTransportSpy(ReloadResponse())
    controller = RemoteBrowserController(transport)

    response = asyncio.run(controller.reload())

    assert response == ReloadResponse()
    assert transport.sent_commands == [ReloadCommand()]


def test_remote_browser_controller_sends_stop_browser_host() -> None:
    transport = BrowserClientTransportSpy(StopBrowserHostResponse())
    controller = RemoteBrowserController(transport)

    response = asyncio.run(controller.stop_browser_host())

    assert response == StopBrowserHostResponse()
    assert transport.sent_commands == [StopBrowserHostCommand()]


def test_remote_browser_controller_sends_press_key() -> None:
    transport = BrowserClientTransportSpy(
        PressKeyResponse(key="Control+A"),
    )
    controller = RemoteBrowserController(transport)

    response = asyncio.run(controller.press_key("Control+A"))

    assert response == PressKeyResponse(key="Control+A")
    [command] = transport.sent_commands
    assert isinstance(command, PressKeyCommand)
    assert command.key == "Control+A"
    assert command.key_down_up_delay_seconds > 0


def test_remote_browser_controller_raises_response_error() -> None:
    transport = BrowserClientTransportSpy(
        BrowserErrorResponse(message="remote failed"),
    )
    controller = RemoteBrowserController(transport)

    with pytest.raises(BrowserOperationError, match="remote failed"):
        asyncio.run(controller.click(10, 20))


def test_remote_browser_controller_rejects_unexpected_response() -> None:
    transport = BrowserClientTransportSpy(ReloadResponse())
    controller = RemoteBrowserController(transport)

    with pytest.raises(
        BrowserOperationError,
        match="unexpected browser response: reload",
    ):
        asyncio.run(controller.click(10, 20))


def test_remote_browser_controller_returns_screenshot_png_bytes() -> None:
    transport = BrowserClientTransportSpy(
        ScreenshotResponse(screenshot_base64="iVBORw0KGgo="),
    )
    controller = RemoteBrowserController(transport)

    screenshot = asyncio.run(controller.screenshot())

    assert transport.sent_commands == [ScreenshotCommand()]
    assert screenshot == b"\x89PNG\r\n\x1a\n"


def test_remote_browser_controller_rejects_invalid_screenshot_base64() -> None:
    transport = BrowserClientTransportSpy(
        ScreenshotResponse(screenshot_base64="invalid!"),
    )
    controller = RemoteBrowserController(transport)

    with pytest.raises(BrowserOperationError, match="valid base64"):
        asyncio.run(controller.screenshot())


def test_browser_command_schema_rejects_unknown_key() -> None:
    with pytest.raises(ValueError, match="extra"):
        ClickCommand.model_validate(
            {
                "type": "click",
                "x": 10,
                "y": 20,
                "hover_delay_seconds": 0.1,
                "mouse_down_up_delay_seconds": 0.1,
                "unexpected": True,
            },
        )


def test_browser_command_schema_rejects_invalid_delay() -> None:
    with pytest.raises(ValueError, match="greater than 0"):
        ClickCommand(
            x=10,
            y=20,
            hover_delay_seconds=0.1,
            mouse_down_up_delay_seconds=0,
        )

    with pytest.raises(ValueError, match="greater than 0"):
        ClickCommand(
            x=10,
            y=20,
            hover_delay_seconds=0,
            mouse_down_up_delay_seconds=0.1,
        )

    with pytest.raises(ValueError, match="greater than 0"):
        TextInputCommand(
            text="abc",
            character_delay_seconds=0,
        )

    with pytest.raises(ValueError, match="at least 1 character"):
        PressKeyCommand(
            key="",
            key_down_up_delay_seconds=0.05,
        )

    with pytest.raises(ValueError, match="greater than 0"):
        PressKeyCommand(
            key="Control+A",
            key_down_up_delay_seconds=0,
        )


def test_browser_response_error_is_distinct_from_success_responses() -> None:
    click = ClickResponse(x=10, y=20)
    goto_url = GotoUrlResponse(url="https://example.invalid/")
    move_mouse = MoveMouseResponse(x=10, y=20)
    text_input = TextInputResponse(text="player@example.invalid")
    press_key = PressKeyResponse(key="Control+A")
    reload = ReloadResponse()
    screenshot = ScreenshotResponse(screenshot_base64="c2NyZWVu")
    stop_browser_host = StopBrowserHostResponse()
    error = BrowserErrorResponse(message="remote failed")

    assert click.type == "click"
    assert goto_url.type == "goto_url"
    assert move_mouse.type == "move_mouse"
    assert text_input.type == "text_input"
    assert press_key.type == "press_key"
    assert reload.type == "reload"
    assert screenshot.type == "screenshot"
    assert screenshot.screenshot_base64 == "c2NyZWVu"
    assert stop_browser_host.type == "stop_browser_host"
    assert error.type == "error"
