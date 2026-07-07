import asyncio
import base64
from typing import override

import pytest

from majsoulrpa.browser.controller import BrowserOperationError
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
    StopBrowserHostCommand,
    StopBrowserHostResponse,
    TextInputCommand,
    TextInputResponse,
    dump_browser_response_json,
    parse_browser_command_json,
)
from majsoulrpa.client.controller_runtime import ControllerRuntimeFactory
from majsoulrpa.config import AppConfig, BrowserConfig, EndpointConfig
from majsoulrpa.presentation import Region
from majsoulrpa.screens import Screen, ScreenDetectionSpec

SYNTHETIC_PNG = b"\x89PNG\r\n\x1a\n"


class MatchingScreen(Screen):
    @override
    async def before_callback(self) -> None:
        pass

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(
            lambda screenshot: screenshot == SYNTHETIC_PNG,
        )


class InputScreen(MatchingScreen):
    async def enter_value(self) -> None:
        await self.fill_region(
            Region(left=0, top=0, width=100, height=100),
            "value",
        )

    async def replace_value(self) -> None:
        await self.fill_region(
            Region(left=0, top=0, width=100, height=100),
            "value",
            clear=True,
        )

    async def move_to_value(self) -> None:
        await self.move_region(Region(left=0, top=0, width=100, height=100))


class ContextCapturedError(RuntimeError):
    def __init__(self, context: object) -> None:
        super().__init__("context captured")
        self.context = context


class ZmqSocketSpy:
    def __init__(self, *responses: BrowserResponse) -> None:
        self.connected_endpoints: list[str] = []
        self.sent_payloads: list[bytes] = []
        self._responses = list(responses)
        self._last_response = responses[-1] if responses else None
        self.closed = False

    def connect(self, endpoint: str) -> None:
        self.connected_endpoints.append(endpoint)

    def close(self, *, linger: int) -> None:
        _ = linger
        self.closed = True

    async def send(self, payload: bytes) -> None:
        self.sent_payloads.append(payload)

    async def recv(self) -> bytes:
        if self._responses:
            response = self._responses.pop(0)
        elif self._last_response is not None:
            response = self._last_response
        else:
            msg = "unexpected recv"
            raise AssertionError(msg)
        return dump_browser_response_json(response)


class ZmqContextSpy:
    def __init__(self, *responses: BrowserResponse) -> None:
        self.socket_spy = ZmqSocketSpy(*responses)
        self.socket_types: list[int] = []
        self.terminated = False

    def socket(self, socket_type: int) -> ZmqSocketSpy:
        self.socket_types.append(socket_type)
        return self.socket_spy

    def term(self) -> None:
        self.terminated = True


def test_controller_runtime_connects_screenshot_and_cleans_up() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode(
                "ascii",
            ),
        ),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig(
        endpoint=EndpointConfig(
            browser_host="192.0.2.10",
            remote_port=12000,
        ),
        browser=BrowserConfig(viewport_height=720),
    )
    runtime = factory({}, config)
    data = object()

    result = asyncio.run(runtime.run(config, data, detection_timeout=0.001))

    assert result is data
    assert context.socket_spy.connected_endpoints == [
        "tcp://192.0.2.10:12000",
    ]
    assert context.socket_spy.closed
    assert context.terminated
    assert context.socket_spy.sent_payloads
    assert [
        parse_browser_command_json(payload)
        for payload in context.socket_spy.sent_payloads
    ] == [ScreenshotCommand()] * len(context.socket_spy.sent_payloads)


def test_controller_runtime_injects_screen_context() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode("ascii"),
        ),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            MatchingScreen: _record_context,
        },
        config,
    )

    with pytest.raises(ContextCapturedError) as exc_info:
        asyncio.run(runtime.run(config, None, detection_timeout=0.001))

    assert exc_info.value.context is not None
    assert context.socket_spy.closed
    assert context.terminated


def test_controller_runtime_screen_helper_sends_click_and_text_input() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode("ascii"),
        ),
        ClickResponse(x=50, y=50),
        TextInputResponse(text="value"),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            InputScreen: _enter_value_and_stop,
        },
        config,
    )

    with pytest.raises(RuntimeError, match="stop"):
        asyncio.run(runtime.run(config, None, detection_timeout=0.001))

    commands = [
        parse_browser_command_json(payload)
        for payload in context.socket_spy.sent_payloads
    ]
    assert isinstance(commands[0], ScreenshotCommand)
    assert isinstance(commands[1], ClickCommand)
    assert isinstance(commands[2], TextInputCommand)
    assert commands[2].text == "value"
    assert context.socket_spy.closed
    assert context.terminated


def test_controller_runtime_can_clear_before_text_input() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode("ascii"),
        ),
        ClickResponse(x=50, y=50),
        PressKeyResponse(key="Control+A"),
        PressKeyResponse(key="Backspace"),
        TextInputResponse(text="value"),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            InputScreen: _replace_value_and_stop,
        },
        config,
    )

    with pytest.raises(RuntimeError, match="stop"):
        asyncio.run(runtime.run(config, None, detection_timeout=0.001))

    commands = [
        parse_browser_command_json(payload)
        for payload in context.socket_spy.sent_payloads
    ]
    assert isinstance(commands[0], ScreenshotCommand)
    assert isinstance(commands[1], ClickCommand)
    assert isinstance(commands[2], PressKeyCommand)
    assert commands[2].key == "ControlOrMeta+A"
    assert commands[2].key_down_up_delay_seconds > 0
    assert isinstance(commands[3], PressKeyCommand)
    assert commands[3].key == "Backspace"
    assert commands[3].key_down_up_delay_seconds > 0
    assert isinstance(commands[4], TextInputCommand)
    assert commands[4].text == "value"


def test_controller_runtime_screen_helper_sends_move_mouse() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode("ascii"),
        ),
        MoveMouseResponse(x=50, y=50),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            InputScreen: _move_to_value_and_stop,
        },
        config,
    )

    with pytest.raises(RuntimeError, match="stop"):
        asyncio.run(runtime.run(config, None, detection_timeout=0.001))

    commands = [
        parse_browser_command_json(payload)
        for payload in context.socket_spy.sent_payloads
    ]
    assert isinstance(commands[0], ScreenshotCommand)
    assert isinstance(commands[1], MoveMouseCommand)
    assert 0 <= commands[1].x < 100
    assert 0 <= commands[1].y < 100


def test_controller_runtime_cleans_up_when_callback_is_cancelled() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode("ascii"),
        ),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            MatchingScreen: _cancel,
        },
        config,
    )

    with pytest.raises(asyncio.CancelledError):
        asyncio.run(runtime.run(config, None, detection_timeout=0.001))

    assert context.socket_spy.closed
    assert context.terminated


def test_controller_runtime_stops_when_screen_requests_stop() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode("ascii"),
        ),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            MatchingScreen: _request_stop,
        },
        config,
    )

    result = asyncio.run(runtime.run(config, "data", detection_timeout=0.001))

    assert result == "stopped"
    assert len(context.socket_spy.sent_payloads) == 1
    assert context.socket_spy.closed
    assert context.terminated


def test_controller_runtime_screen_helper_sends_stop_browser_host() -> None:
    context = ZmqContextSpy(
        ScreenshotResponse(
            screenshot_base64=base64.b64encode(SYNTHETIC_PNG).decode("ascii"),
        ),
        StopBrowserHostResponse(),
    )
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            MatchingScreen: _stop_browser_host_and_stop_rpa,
        },
        config,
    )

    result = asyncio.run(runtime.run(config, "data", detection_timeout=0.001))

    assert result == "stopped"
    commands = [
        parse_browser_command_json(payload)
        for payload in context.socket_spy.sent_payloads
    ]
    assert isinstance(commands[0], ScreenshotCommand)
    assert isinstance(commands[1], StopBrowserHostCommand)
    assert context.socket_spy.closed
    assert context.terminated


def test_controller_runtime_propagates_remote_error_response() -> None:
    context = ZmqContextSpy(BrowserErrorResponse(message="remote failed"))
    factory = ControllerRuntimeFactory(context_factory=lambda: context)
    config = AppConfig()
    runtime = factory(
        {
            MatchingScreen: _record_context,
        },
        config,
    )

    with pytest.raises(BrowserOperationError, match="remote failed"):
        asyncio.run(runtime.run(config, None, detection_timeout=0.001))

    assert context.socket_spy.closed
    assert context.terminated


async def _record_context(screen: MatchingScreen, _data: object) -> object:
    raise ContextCapturedError(screen.context)


async def _enter_value_and_stop(
    screen: InputScreen,
    _data: object,
) -> object:
    await screen.enter_value()
    msg = "stop"
    raise RuntimeError(msg)


async def _replace_value_and_stop(
    screen: InputScreen,
    _data: object,
) -> object:
    await screen.replace_value()
    msg = "stop"
    raise RuntimeError(msg)


async def _move_to_value_and_stop(
    screen: InputScreen,
    _data: object,
) -> object:
    await screen.move_to_value()
    msg = "stop"
    raise RuntimeError(msg)


async def _cancel(_screen: MatchingScreen, _data: object) -> object:
    raise asyncio.CancelledError


async def _request_stop(screen: MatchingScreen, _data: object) -> object:
    await screen.context.request_stop()
    return "stopped"


async def _stop_browser_host_and_stop_rpa(
    screen: MatchingScreen,
    _data: object,
) -> object:
    await screen.stop_browser_host()
    await screen.stop_rpa()
    return "stopped"
