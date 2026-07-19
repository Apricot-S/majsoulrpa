import asyncio
import logging
from collections import deque
from dataclasses import replace
from inspect import signature

import pytest
from pydantic import JsonValue

import majsoulrpa.screens.room.screen as room_module
from majsoulrpa.assets.templates.room import (
    LEAVE_SETTINGS_PATH,
    LEAVE_TEMPLATE_PATH,
)
from majsoulrpa.screens import (
    ScreenContext,
    ScreenDetectionError,
    ScreenInconsistentMessageError,
    ScreenStaleError,
)
from majsoulrpa.screens.room import (
    RoomOperation,
    RoomOperationFailureReason,
    RoomOperationRejectedError,
    RoomScreen,
    RoomStatus,
)
from majsoulrpa.sniffer.events import DecodedSnifferMessage, Direction
from tests.screens._support import (
    BrowserControllerSpy,
    _notice,
    _request_response,
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)
from tests.screens.room.test_state_api import _AccountState, _room


class _OperationMessageSource:
    def __init__(
        self,
        queued: tuple[DecodedSnifferMessage, ...],
        waiting: tuple[DecodedSnifferMessage, ...],
    ) -> None:
        self._queued = deque(queued)
        self._waiting = deque(waiting)
        self.get_count = 0

    async def get(self) -> DecodedSnifferMessage:
        self.get_count += 1
        if self._waiting:
            return self._waiting.popleft()
        future: asyncio.Future[DecodedSnifferMessage] = (
            asyncio.get_running_loop().create_future()
        )
        return await future

    def get_nowait(self) -> DecodedSnifferMessage | None:
        if not self._queued:
            return None
        return self._queued.popleft()

    def put_back(self, message: DecodedSnifferMessage) -> None:
        self._queued.appendleft(message)

    def enqueue(self, message: DecodedSnifferMessage) -> None:
        self._queued.append(message)


@pytest.mark.parametrize("self_account_id", [100001, 100002])
def test_leave_clicks_ui_and_stales_after_success(
    self_account_id: int,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr(room_module.asyncio, "sleep", sleep)
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_request_response(".lq.Lobby.leaveRoom", {}),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=LEAVE_TEMPLATE_PATH,
            settings_path=LEAVE_SETTINGS_PATH,
        ),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(self_account_id),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    result = asyncio.run(screen.leave())

    assert result is None
    assert sleeps == [1.0]
    assert len(browser.clicked_points) == 1
    assert messages.get_count == 1
    state = context.room_state_cache.state
    assert state is not None
    assert state.status is RoomStatus.LEFT
    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.get_state())


def test_leave_does_not_use_historical_leave_response() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_request_response(".lq.Lobby.leaveRoom", {}),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=LEAVE_TEMPLATE_PATH,
            settings_path=LEAVE_SETTINGS_PATH,
        ),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())
    messages.enqueue(_request_response(".lq.Lobby.leaveRoom", {}))

    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.leave())

    assert browser.clicked_points == []
    assert messages.get_count == 0
    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is RoomStatus.LEFT


def test_leave_server_rejection_keeps_screen_active(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(
            _request_response(
                ".lq.Lobby.leaveRoom",
                {"error": {"code": 9999, "message": "sensitive"}},
            ),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=LEAVE_TEMPLATE_PATH,
            settings_path=LEAVE_SETTINGS_PATH,
        ),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    with (
        caplog.at_level(
            logging.WARNING,
            logger="majsoulrpa.screens.room.screen",
        ),
        pytest.raises(RoomOperationRejectedError) as exc_info,
    ):
        asyncio.run(screen.leave())

    error = exc_info.value
    assert error.operation is RoomOperation.LEAVE
    assert error.reason is RoomOperationFailureReason.UNRECOGNIZED_ERROR_CODE
    assert error.server_error_code == 9999
    assert "sensitive" not in str(error)
    assert "9999" in caplog.text
    state = asyncio.run(screen.get_state())
    assert state.status is RoomStatus.WAITING


@pytest.mark.parametrize(
    "error",
    [None, {}, {"code": True}, {"code": "invalid"}],
)
def test_leave_rejects_malformed_server_error(error: JsonValue) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_request_response(".lq.Lobby.leaveRoom", {"error": error}),),
    )
    screenshot = _synthetic_template_screenshot(
        template_path=LEAVE_TEMPLATE_PATH,
        settings_path=LEAVE_SETTINGS_PATH,
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.leave())

    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_leave_does_not_click_after_room_becomes_inactive() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=LEAVE_TEMPLATE_PATH,
            settings_path=LEAVE_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())
    messages.enqueue(_notice(".lq.NotifyRoomGameStart"))

    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.leave())

    assert browser.clicked_points == []


def test_kick_interrupts_leave_wait() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_notice(".lq.NotifyRoomKickOut"),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=LEAVE_TEMPLATE_PATH,
            settings_path=LEAVE_SETTINGS_PATH,
        ),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.leave())

    assert len(browser.clicked_points) == 1
    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is RoomStatus.KICKED


def test_leave_requires_outbound_request_response() -> None:
    response = _request_response(".lq.Lobby.leaveRoom", {})
    inbound_response = replace(
        response,
        raw=replace(response.raw, request_direction=Direction.INBOUND),
    )
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(inbound_response,),
    )
    screenshot = _synthetic_template_screenshot(
        template_path=LEAVE_TEMPLATE_PATH,
        settings_path=LEAVE_SETTINGS_PATH,
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.leave())

    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_leave_cancellation_keeps_waiting_state_active() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=LEAVE_TEMPLATE_PATH,
            settings_path=LEAVE_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())

    async def leave_with_timeout() -> None:
        async with asyncio.timeout(0.001):
            await screen.leave()

    with pytest.raises(TimeoutError):
        asyncio.run(leave_with_timeout())

    assert len(browser.clicked_points) == 1
    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_leave_requires_leave_template() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_request_response(".lq.Lobby.leaveRoom", {}),),
    )
    browser = BrowserControllerSpy(_synthetic_blank_screenshot())
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenDetectionError):
        asyncio.run(screen.leave())

    assert browser.clicked_points == []
    assert messages.get_count == 0
    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_leave_has_no_timeout_argument_and_safe_api_log(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_request_response(".lq.Lobby.leaveRoom", {}),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=LEAVE_TEMPLATE_PATH,
            settings_path=LEAVE_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        asyncio.run(screen.leave())

    assert list(signature(RoomScreen.leave).parameters) == ["self"]
    api_messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert api_messages == ["screen API called: screen=RoomScreen api=leave"]
