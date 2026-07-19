import asyncio
import logging
from dataclasses import replace
from inspect import signature

import pytest
from pydantic import JsonValue

import majsoulrpa.screens.room.screen as room_module
from majsoulrpa.assets.templates.room import (
    ROOM_SIGN_SETTINGS_PATH,
    ROOM_SIGN_TEMPLATE_PATH,
    START_SETTINGS_PATH,
    START_TEMPLATE_PATH,
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
    RoomOperationNotAllowedError,
    RoomOperationNotAllowedReason,
    RoomOperationRejectedError,
    RoomScreen,
    RoomStatus,
)
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedSnifferMessage,
    Direction,
)
from tests.screens._support import (
    BrowserControllerSpy,
    _request_response,
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)
from tests.screens.room.test_leave import _OperationMessageSource
from tests.screens.room.test_state_api import _AccountState, _notice, _room


def _startable_room() -> dict[str, JsonValue]:
    room = _room()
    room["ready_list"] = [100002]
    room["robots"] = [{}, {}]
    return room


def _player_update(
    *,
    owner_id: int = 100001,
    ai_count: int = 2,
) -> DecodedNotice:
    return _notice(
        ".lq.NotifyRoomPlayerUpdate",
        {
            "owner_id": owner_id,
            "player_list": [
                {"account_id": 100001, "nickname": "host"},
                {"account_id": 100002, "nickname": "guest"},
            ],
            "robots": [{}] * ai_count,
            "positions": [],
        },
    )


class _FailingScreenshotBrowser(BrowserControllerSpy):
    async def screenshot(self) -> bytes:
        msg = "synthetic browser infrastructure failure"
        raise RuntimeError(msg)


def test_start_match_clicks_start_and_stales_after_response_and_notice(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr(room_module.asyncio, "sleep", sleep)
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(
            _request_response(".lq.Lobby.startRoom", {}),
            _notice(".lq.NotifyRoomGameStart"),
        ),
    )
    start_screenshot = _synthetic_template_screenshot(
        template_path=START_TEMPLATE_PATH,
        settings_path=START_SETTINGS_PATH,
    )
    room_screenshot = _synthetic_template_screenshot(
        template_path=ROOM_SIGN_TEMPLATE_PATH,
        settings_path=ROOM_SIGN_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(
        start_screenshot,
        room_screenshot,
        _synthetic_blank_screenshot(),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    result = asyncio.run(screen.start_match())

    assert result is None
    assert len(browser.clicked_points) == 1
    assert messages.get_count == 2
    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is RoomStatus.MATCH_STARTED
    assert sleeps == [room_module.TEMPLATE_DETECTION_RETRY_INTERVAL_SECONDS]
    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.get_state())


def test_start_match_waits_while_room_screen_remains_visible() -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(
            _request_response(".lq.Lobby.startRoom", {}),
            _notice(".lq.NotifyRoomGameStart"),
        ),
    )
    start_screenshot = _synthetic_template_screenshot(
        template_path=START_TEMPLATE_PATH,
        settings_path=START_SETTINGS_PATH,
    )
    room_screenshot = _synthetic_template_screenshot(
        template_path=ROOM_SIGN_TEMPLATE_PATH,
        settings_path=ROOM_SIGN_SETTINGS_PATH,
    )
    browser = BrowserControllerSpy(start_screenshot, room_screenshot)
    browser.screenshot_bytes = room_screenshot
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    async def start_match_with_timeout() -> None:
        async with asyncio.timeout(0.001):
            await screen.start_match()

    with pytest.raises(TimeoutError):
        asyncio.run(start_match_with_timeout())

    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is RoomStatus.MATCH_STARTED
    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.get_state())


@pytest.mark.parametrize(
    ("self_account_id", "ready", "ai_count", "expected_reason"),
    [
        (100002, True, 2, RoomOperationNotAllowedReason.NOT_HOST),
        (100001, True, 0, RoomOperationNotAllowedReason.ROOM_NOT_FULL),
        (100001, False, 2, RoomOperationNotAllowedReason.GUEST_NOT_READY),
    ],
)
def test_start_match_rejects_failed_precondition_without_clicking(
    self_account_id: int,
    ready: bool,  # noqa: FBT001
    ai_count: int,
    expected_reason: RoomOperationNotAllowedReason,
) -> None:
    room = _room()
    room["ready_list"] = [100002] if ready else []
    room["robots"] = [{}] * ai_count
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": room}),),
        waiting=(),
    )
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(self_account_id),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(RoomOperationNotAllowedError) as exc_info:
        asyncio.run(screen.start_match())

    assert exc_info.value.operation is RoomOperation.START_MATCH
    assert exc_info.value.reason is expected_reason
    assert browser.clicked_points == []
    assert messages.get_count == 0


def test_start_match_accepts_game_start_notice_before_response() -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(
            _notice(".lq.NotifyRoomGameStart"),
            _request_response(".lq.Lobby.startRoom", {}),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
        ),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    asyncio.run(screen.start_match())

    assert messages.get_count == 2
    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is RoomStatus.MATCH_STARTED


@pytest.mark.parametrize(
    ("waiting", "expected_status", "expected_stale"),
    [
        (
            (_request_response(".lq.Lobby.startRoom", {}),),
            RoomStatus.WAITING,
            False,
        ),
        (
            (_notice(".lq.NotifyRoomGameStart"),),
            RoomStatus.MATCH_STARTED,
            True,
        ),
    ],
)
def test_start_match_waits_for_response_and_game_start_notice(
    waiting: tuple[DecodedSnifferMessage, ...],
    expected_status: RoomStatus,
    expected_stale: bool,  # noqa: FBT001
) -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=waiting,
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
        ),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    async def start_match_with_timeout() -> None:
        async with asyncio.timeout(0.001):
            await screen.start_match()

    with pytest.raises(TimeoutError):
        asyncio.run(start_match_with_timeout())

    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is expected_status
    if expected_stale:
        with pytest.raises(ScreenStaleError):
            asyncio.run(screen.get_state())
    else:
        assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


@pytest.mark.parametrize(
    ("update", "expected_reason"),
    [
        (
            _player_update(owner_id=100002),
            RoomOperationNotAllowedReason.NOT_HOST,
        ),
        (
            _player_update(ai_count=0),
            RoomOperationNotAllowedReason.ROOM_NOT_FULL,
        ),
        (
            _notice(
                ".lq.NotifyRoomPlayerReady",
                {"account_id": 100002, "ready": False},
            ),
            RoomOperationNotAllowedReason.GUEST_NOT_READY,
        ),
    ],
)
def test_start_match_uses_latest_state_before_clicking(
    update: DecodedSnifferMessage,
    expected_reason: RoomOperationNotAllowedReason,
) -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(),
    )
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())
    messages.enqueue(update)

    with pytest.raises(RoomOperationNotAllowedError) as exc_info:
        asyncio.run(screen.start_match())

    assert exc_info.value.reason is expected_reason
    assert browser.clicked_points == []
    assert messages.get_count == 0


def test_start_match_does_not_use_historical_start_response() -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(
            _request_response(".lq.Lobby.startRoom", {}),
            _notice(".lq.NotifyRoomGameStart"),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
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
    messages.enqueue(_request_response(".lq.Lobby.startRoom", {}))

    asyncio.run(screen.start_match())

    assert len(browser.clicked_points) == 1
    assert messages.get_count == 2


def test_start_match_server_rejection_keeps_screen_active() -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(
            _request_response(
                ".lq.Lobby.startRoom",
                {"error": {"code": 9999, "message": "sensitive"}},
            ),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
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

    with pytest.raises(RoomOperationRejectedError) as exc_info:
        asyncio.run(screen.start_match())

    error = exc_info.value
    assert error.operation is RoomOperation.START_MATCH
    assert error.reason is RoomOperationFailureReason.UNRECOGNIZED_ERROR_CODE
    assert error.server_error_code == 9999
    assert "sensitive" not in str(error)
    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


@pytest.mark.parametrize(
    "error",
    [None, {}, {"code": True}, {"code": "invalid"}],
)
def test_start_match_rejects_malformed_server_error(error: JsonValue) -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(_request_response(".lq.Lobby.startRoom", {"error": error}),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
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

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.start_match())

    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_start_match_requires_outbound_request_response() -> None:
    response = _request_response(".lq.Lobby.startRoom", {})
    response = replace(
        response,
        raw=replace(response.raw, request_direction=Direction.INBOUND),
    )
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(response,),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
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

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.start_match())

    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_start_match_requires_start_template() -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(),
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
        asyncio.run(screen.start_match())

    assert browser.clicked_points == []
    assert messages.get_count == 0
    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_start_match_does_not_convert_browser_failure() -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=_FailingScreenshotBrowser(b"unused"),
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(
        RuntimeError,
        match="synthetic browser infrastructure failure",
    ):
        asyncio.run(screen.start_match())


def test_kick_interrupts_start_match_wait() -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(_notice(".lq.NotifyRoomKickOut"),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
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
        asyncio.run(screen.start_match())

    assert len(browser.clicked_points) == 1
    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is RoomStatus.KICKED


def test_start_match_has_no_arguments_and_safe_api_log(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _OperationMessageSource(
        queued=(
            _request_response(
                ".lq.Lobby.createRoom",
                {"room": _startable_room()},
            ),
        ),
        waiting=(
            _request_response(".lq.Lobby.startRoom", {}),
            _notice(".lq.NotifyRoomGameStart"),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=START_TEMPLATE_PATH,
            settings_path=START_SETTINGS_PATH,
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
        asyncio.run(screen.start_match())

    assert list(signature(RoomScreen.start_match).parameters) == ["self"]
    api_messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert api_messages == [
        "screen API called: screen=RoomScreen api=start_match",
    ]
