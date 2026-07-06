import asyncio

import pytest

from majsoulrpa.browser import (
    BrowserCommand,
    BrowserRequestHandler,
    BrowserResponse,
    ClickCommand,
    ClickResponse,
    TextInputCommand,
    TextInputResponse,
)


class BrowserRequestTransportSpy:
    def __init__(self, *commands: BrowserCommand) -> None:
        self._commands = list(commands)
        self.sent_responses: list[BrowserResponse] = []

    async def recv_command(self) -> BrowserCommand:
        if not self._commands:
            raise asyncio.CancelledError
        return self._commands.pop(0)

    async def send_response(self, response: BrowserResponse) -> None:
        self.sent_responses.append(response)


class BrowserCommandExecutorSpy:
    def __init__(self, *responses: BrowserResponse) -> None:
        self._responses = list(responses)
        self.executed_commands: list[BrowserCommand] = []

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        self.executed_commands.append(command)
        return self._responses.pop(0)


def test_browser_request_handler_executes_command_and_sends_response() -> None:
    command = ClickCommand(
        x=25,
        y=40,
        mouse_down_up_delay_seconds=0.1,
    )
    response = ClickResponse(x=25, y=40)
    transport = BrowserRequestTransportSpy(command)
    executor = BrowserCommandExecutorSpy(response)
    handler = BrowserRequestHandler(transport, executor)

    asyncio.run(handler.handle_once())

    assert executor.executed_commands == [command]
    assert transport.sent_responses == [response]


def test_browser_request_handler_serves_until_cancelled() -> None:
    click_command = ClickCommand(
        x=25,
        y=40,
        mouse_down_up_delay_seconds=0.1,
    )
    text_command = TextInputCommand(
        text="player@example.invalid",
        character_delay_seconds=0.05,
    )
    click_response = ClickResponse(x=25, y=40)
    text_response = TextInputResponse(text="player@example.invalid")
    transport = BrowserRequestTransportSpy(click_command, text_command)
    executor = BrowserCommandExecutorSpy(click_response, text_response)
    handler = BrowserRequestHandler(transport, executor)

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(handler.serve_forever())

    assert executor.executed_commands == [click_command, text_command]
    assert transport.sent_responses == [click_response, text_response]


def test_browser_request_handler_does_not_hide_cancellation() -> None:
    transport = BrowserRequestTransportSpy()
    executor = BrowserCommandExecutorSpy()
    handler = BrowserRequestHandler(transport, executor)

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(handler.handle_once())
