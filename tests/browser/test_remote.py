import asyncio
from random import Random

import pytest

from majsoulrpa.browser import (
    BrowserCommand,
    BrowserErrorResponse,
    BrowserOperationError,
    ClickCommand,
    ClickResponse,
    RemoteBrowserController,
    ScreenshotCommand,
    ScreenshotResponse,
    TextInputCommand,
    TextInputResponse,
)


class BrowserTransportSpy:
    def __init__(
        self,
        *responses: (
            ClickResponse
            | TextInputResponse
            | ScreenshotResponse
            | BrowserErrorResponse
        ),
    ) -> None:
        self.sent_commands: list[BrowserCommand] = []
        self._responses = list(responses)

    async def send(self, command: BrowserCommand) -> None:
        self.sent_commands.append(command)

    async def recv(
        self,
    ) -> (
        ClickResponse
        | TextInputResponse
        | ScreenshotResponse
        | BrowserErrorResponse
    ):
        return self._responses.pop(0)


def test_remote_browser_controller_sends_click_and_text_input() -> None:
    transport = BrowserTransportSpy(
        ClickResponse(x=25, y=40),
        TextInputResponse(text="player@example.invalid"),
    )
    controller = RemoteBrowserController(transport, rng=Random(0))

    asyncio.run(controller.click(25, 40))
    asyncio.run(controller.input_text("ab"))

    click_command, text_command = transport.sent_commands
    assert isinstance(click_command, ClickCommand)
    assert isinstance(text_command, TextInputCommand)
    assert click_command == ClickCommand(
        x=25,
        y=40,
        mouse_down_up_delay_seconds=click_command.mouse_down_up_delay_seconds,
    )
    assert click_command.mouse_down_up_delay_seconds > 0
    assert text_command == TextInputCommand(
        text="ab",
        character_delay_seconds=text_command.character_delay_seconds,
    )
    assert text_command.character_delay_seconds > 0


def test_remote_browser_controller_raises_response_error() -> None:
    transport = BrowserTransportSpy(
        BrowserErrorResponse(message="remote failed"),
    )
    controller = RemoteBrowserController(transport)

    with pytest.raises(BrowserOperationError, match="remote failed"):
        asyncio.run(controller.click(10, 20))


def test_remote_browser_controller_takes_screenshot_explicitly() -> None:
    transport = BrowserTransportSpy(
        ScreenshotResponse(screenshot_base64="c2NyZWVu"),
    )
    controller = RemoteBrowserController(transport)

    response = asyncio.run(controller.take_screenshot())

    assert transport.sent_commands == [ScreenshotCommand()]
    assert response.screenshot_base64 == "c2NyZWVu"


def test_browser_command_schema_rejects_unknown_key() -> None:
    with pytest.raises(ValueError, match="extra"):
        ClickCommand.model_validate(
            {
                "type": "click",
                "x": 10,
                "y": 20,
                "mouse_down_up_delay_seconds": 0.1,
                "unexpected": True,
            },
        )


def test_browser_command_schema_rejects_invalid_delay() -> None:
    with pytest.raises(ValueError, match="greater than 0"):
        ClickCommand(
            x=10,
            y=20,
            mouse_down_up_delay_seconds=0,
        )

    with pytest.raises(ValueError, match="greater than 0"):
        TextInputCommand(
            text="abc",
            character_delay_seconds=0,
        )


def test_browser_response_error_is_distinct_from_success_responses() -> None:
    click = ClickResponse(x=10, y=20)
    text_input = TextInputResponse(text="player@example.invalid")
    screenshot = ScreenshotResponse(screenshot_base64="c2NyZWVu")
    error = BrowserErrorResponse(message="remote failed")

    assert click.type == "click"
    assert text_input.type == "text_input"
    assert screenshot.type == "screenshot"
    assert screenshot.screenshot_base64 == "c2NyZWVu"
    assert error.type == "error"
