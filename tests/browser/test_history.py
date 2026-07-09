import asyncio
import logging

import pytest

from majsoulrpa.browser.history import (
    LoggingBrowserClientTransport,
    LoggingBrowserCommandExecutor,
    summarize_browser_command,
    summarize_browser_response,
)
from majsoulrpa.browser.messages import (
    BrowserCommand,
    BrowserResponse,
    GotoUrlCommand,
    GotoUrlResponse,
    ScreenshotResponse,
    TextInputCommand,
    TextInputResponse,
)


class BrowserClientTransportSpy:
    def __init__(self, response: BrowserResponse) -> None:
        self.sent_commands: list[BrowserCommand] = []
        self._response = response

    async def send_command(self, command: BrowserCommand) -> None:
        self.sent_commands.append(command)

    async def recv_response(self) -> BrowserResponse:
        return self._response


class BrowserCommandExecutorSpy:
    def __init__(self, response: BrowserResponse) -> None:
        self.executed_commands: list[BrowserCommand] = []
        self._response = response

    async def execute(self, command: BrowserCommand) -> BrowserResponse:
        self.executed_commands.append(command)
        return self._response


def test_browser_history_summarizes_sensitive_payloads() -> None:
    command = TextInputCommand(
        text="player@example.invalid",
        character_delay_seconds=0.05,
    )
    response = ScreenshotResponse(screenshot_base64="secret-base64")

    assert summarize_browser_command(command) == {
        "type": "text_input",
        "text_length": 22,
        "character_delay_seconds": 0.05,
    }
    assert summarize_browser_response(response) == {
        "type": "screenshot",
        "screenshot_base64_length": 13,
    }


def test_browser_history_keeps_goto_url_for_log_id() -> None:
    url = "https://game.mahjongsoul.com/?paipu=synthetic-log-id"

    assert summarize_browser_command(GotoUrlCommand(url=url)) == {
        "type": "goto_url",
        "url": url,
    }
    assert summarize_browser_response(GotoUrlResponse(url=url)) == {
        "type": "goto_url",
        "url": url,
    }


def test_logging_browser_client_transport_redacts_text_and_screenshot(
    caplog: pytest.LogCaptureFixture,
) -> None:
    transport = BrowserClientTransportSpy(
        ScreenshotResponse(screenshot_base64="secret-base64"),
    )
    logging_transport = LoggingBrowserClientTransport(transport)
    command = TextInputCommand(
        text="player@example.invalid",
        character_delay_seconds=0.05,
    )

    with caplog.at_level(logging.DEBUG, logger="majsoulrpa.browser.client"):
        asyncio.run(logging_transport.send_command(command))
        response = asyncio.run(logging_transport.recv_response())

    assert transport.sent_commands == [command]
    assert response == ScreenshotResponse(screenshot_base64="secret-base64")
    log_text = caplog.text
    assert "browser client command" in log_text
    assert "browser client response" in log_text
    assert "text_length" in log_text
    assert "screenshot_base64_length" in log_text
    assert "player@example.invalid" not in log_text
    assert "secret-base64" not in log_text


def test_logging_browser_command_executor_redacts_text_and_response(
    caplog: pytest.LogCaptureFixture,
) -> None:
    executor = BrowserCommandExecutorSpy(
        TextInputResponse(text="player@example.invalid"),
    )
    logging_executor = LoggingBrowserCommandExecutor(executor)
    command = TextInputCommand(
        text="player@example.invalid",
        character_delay_seconds=0.05,
    )

    with caplog.at_level(logging.DEBUG, logger="majsoulrpa.browser.host"):
        response = asyncio.run(logging_executor.execute(command))

    assert executor.executed_commands == [command]
    assert response == TextInputResponse(text="player@example.invalid")
    log_text = caplog.text
    assert "browser host command" in log_text
    assert "browser host response" in log_text
    assert "text_length" in log_text
    assert "player@example.invalid" not in log_text
