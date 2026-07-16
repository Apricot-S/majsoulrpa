import asyncio
import datetime
import logging
from dataclasses import dataclass, replace
from inspect import Parameter, signature

import pytest
from pydantic import JsonValue

import majsoulrpa.screens.room.screen as room_module
from majsoulrpa.screens import (
    ScreenContext,
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenStaleError,
)
from majsoulrpa.screens.room import RoomScreen, RoomStatus
from majsoulrpa.screens.room._decode import RoomStateDecodeError
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedSnifferMessage,
    Direction,
    RawNotice,
)
from tests.screens.home._support import (
    BrowserControllerSpy,
    _message_queue,
    _request_response,
)
from tests.sniffer.fakes import EMPTY_SNIFFER_MESSAGES


@dataclass
class _AccountState:
    account_id: int | None


class _WaitingMessageSource:
    def __init__(self, message: DecodedSnifferMessage) -> None:
        self._message = message
        self.get_count = 0

    async def get(self) -> DecodedSnifferMessage:
        self.get_count += 1
        return self._message

    def get_nowait(self) -> None:
        return None

    def put_back(self, message: DecodedSnifferMessage) -> None:
        _ = message


class _FailingMessageSource:
    async def get(self) -> DecodedSnifferMessage:
        msg = "synthetic infrastructure failure"
        raise RuntimeError(msg)

    def get_nowait(self) -> None:
        return None

    def put_back(self, message: DecodedSnifferMessage) -> None:
        _ = message


class _TimeoutFailingMessageSource:
    async def get(self) -> DecodedSnifferMessage:
        msg = "synthetic infrastructure timeout"
        raise TimeoutError(msg)

    def get_nowait(self) -> None:
        return None

    def put_back(self, message: DecodedSnifferMessage) -> None:
        _ = message


class _QueuedThenWaitingMessageSource:
    def __init__(
        self,
        queued: DecodedSnifferMessage,
        waiting: DecodedSnifferMessage,
    ) -> None:
        self._queued: DecodedSnifferMessage | None = queued
        self._waiting = waiting
        self.get_count = 0

    async def get(self) -> DecodedSnifferMessage:
        self.get_count += 1
        return self._waiting

    def get_nowait(self) -> DecodedSnifferMessage | None:
        message = self._queued
        self._queued = None
        return message

    def put_back(self, message: DecodedSnifferMessage) -> None:
        _ = message


class _UpdateThenBlockingMessageSource:
    def __init__(
        self,
        queued: DecodedSnifferMessage,
        update: DecodedSnifferMessage,
    ) -> None:
        self._queued: DecodedSnifferMessage | None = queued
        self._update: DecodedSnifferMessage | None = update

    async def get(self) -> DecodedSnifferMessage:
        if self._update is not None:
            message = self._update
            self._update = None
            return message
        future: asyncio.Future[DecodedSnifferMessage] = (
            asyncio.get_running_loop().create_future()
        )
        return await future

    def get_nowait(self) -> DecodedSnifferMessage | None:
        message = self._queued
        self._queued = None
        return message

    def put_back(self, message: DecodedSnifferMessage) -> None:
        _ = message


def _room(*, room_id: int = 12345) -> dict[str, JsonValue]:
    return {
        "room_id": room_id,
        "owner_id": 100001,
        "max_player_count": 4,
        "persons": [
            {"account_id": 100001, "nickname": "host"},
            {"account_id": 100002, "nickname": "self"},
        ],
        "ready_list": [],
        "robot_count": 0,
        "robots": [],
    }


def _notice(
    name: str,
    message: dict[str, JsonValue] | None = None,
) -> DecodedNotice:
    return DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=name,
            payload=b"synthetic-notice",
            observed_at=datetime.datetime(
                2026,
                1,
                2,
                tzinfo=datetime.UTC,
            ),
        ),
        message={} if message is None else message,
    )


def _ready_notice() -> DecodedNotice:
    return _notice(
        ".lq.NotifyRoomPlayerReady",
        {"account_id": 100002, "ready": True},
    )


def _host_change_notice() -> DecodedNotice:
    return _notice(
        ".lq.NotifyRoomPlayerUpdate",
        {
            "owner_id": 100002,
            "robot_count": 0,
            "player_list": [
                {"account_id": 100001, "nickname": "former-host"},
                {"account_id": 100002, "nickname": "self"},
            ],
            "robots": [],
            "positions": [],
        },
    )


def test_before_callback_drains_accumulated_room_messages_in_order() -> None:
    messages = _message_queue(
        _request_response(".lq.Lobby.joinRoom", {"room": _room()}),
        _ready_notice(),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100002),
    )
    screen = RoomScreen(context=context)

    asyncio.run(screen.before_callback())

    state = context.room_state_cache.state
    assert state is not None
    assert state.version == 2
    assert state.players[1].is_ready is True
    assert messages.get_nowait() is None


def test_before_callback_waits_for_initial_room_snapshot() -> None:
    messages = _WaitingMessageSource(
        _request_response(".lq.Lobby.createRoom", {"room": _room()}),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)

    asyncio.run(screen.before_callback())

    assert context.room_state_cache.state is not None
    assert messages.get_count == 1


def test_get_state_drains_messages_without_browser_operation() -> None:
    messages = _message_queue(
        _request_response(".lq.Lobby.joinRoom", {"room": _room()}),
    )
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100002),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())
    messages.enqueue(_ready_notice())

    state = asyncio.run(screen.get_state())

    assert state.version == 2
    assert state.players[1].is_ready is True
    assert browser.clicked_points == []
    assert browser.screenshot_count == 0


def test_room_state_update_error_logs_message_before_inconsistent_error(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _message_queue(
        _request_response(".lq.Lobby.joinRoom", {"room": _room()}),
    )
    screenshot = b"synthetic-screenshot"
    context = ScreenContext(
        browser=BrowserControllerSpy(screenshot),
        sniffer_messages=messages,
        account_state=_AccountState(100002),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())
    malformed_notice = _ready_notice()
    malformed_notice.message["ready"] = "invalid"
    messages.enqueue(malformed_notice)

    with (
        caplog.at_level(
            logging.INFO,
            logger="majsoulrpa.screens.room.screen",
        ),
        pytest.raises(ScreenInconsistentMessageError) as exc_info,
    ):
        asyncio.run(screen.get_state())

    assert exc_info.value.screenshot == screenshot
    assert isinstance(exc_info.value.__cause__, RoomStateDecodeError)
    messages_logged = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.room.screen"
    ]
    assert len(messages_logged) == 1
    assert messages_logged[0].startswith("Sniffer message: ")
    assert ".lq.NotifyRoomPlayerReady" in messages_logged[0]
    assert '"ready":"invalid"' in messages_logged[0]


def test_room_screen_instances_share_latest_context_state() -> None:
    messages = _message_queue(
        _request_response(".lq.Lobby.createRoom", {"room": _room()}),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    first = RoomScreen(context=context)
    asyncio.run(first.before_callback())
    second = RoomScreen(context=context)

    asyncio.run(second.before_callback())

    assert asyncio.run(second.get_state()) is asyncio.run(first.get_state())


def test_old_room_screen_generation_becomes_stale_for_new_room() -> None:
    messages = _message_queue(
        _request_response(".lq.Lobby.createRoom", {"room": _room()}),
    )
    screenshot = b"synthetic-screenshot"
    context = ScreenContext(
        browser=BrowserControllerSpy(screenshot),
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    old_screen = RoomScreen(context=context)
    asyncio.run(old_screen.before_callback())
    messages.enqueue(_notice(".lq.NotifyRoomKickOut"))
    messages.enqueue(
        _request_response(
            ".lq.Lobby.createRoom",
            {"room": _room(room_id=54321)},
        ),
    )

    with pytest.raises(ScreenStaleError) as exc_info:
        asyncio.run(old_screen.get_state())

    assert exc_info.value.screenshot == screenshot
    new_screen = RoomScreen(context=context)
    asyncio.run(new_screen.before_callback())
    assert asyncio.run(new_screen.get_state()).room_id == 54321


def test_before_callback_fails_when_initial_snapshot_does_not_arrive(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    screenshot = b"synthetic-screenshot"
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            sniffer_messages=EMPTY_SNIFFER_MESSAGES,
            account_state=_AccountState(100001),
        ),
    )
    monkeypatch.setattr(
        room_module,
        "ROOM_STATE_INITIALIZATION_TIMEOUT_SECONDS",
        0.001,
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == screenshot
    assert isinstance(exc_info.value.__cause__, TimeoutError)


def test_before_callback_rejects_missing_self_account_id() -> None:
    screenshot = b"synthetic-screenshot"
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            sniffer_messages=_message_queue(
                _request_response(
                    ".lq.Lobby.joinRoom",
                    {"room": _room()},
                ),
            ),
            account_state=_AccountState(None),
        ),
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == screenshot


def test_get_state_has_no_timeout_and_logs_no_room_identifiers(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _message_queue(
        _request_response(".lq.Lobby.createRoom", {"room": _room()}),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        state = asyncio.run(screen.get_state())

    assert list(signature(RoomScreen.get_state).parameters) == ["self"]
    api_messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert api_messages == [
        "screen API called: screen=RoomScreen api=get_state",
    ]
    assert str(state.room_id) not in api_messages[0]
    assert str(state.self_account_id) not in api_messages[0]
    assert all(player.name not in api_messages[0] for player in state.players)


def test_malformed_initial_snapshot_becomes_inconsistent_message_error() -> (
    None
):
    room = _room()
    room["max_player_count"] = "invalid"
    screenshot = b"synthetic-screenshot"
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            sniffer_messages=_message_queue(
                _request_response(
                    ".lq.Lobby.createRoom",
                    {"room": room},
                ),
            ),
            account_state=_AccountState(100001),
        ),
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == screenshot
    assert isinstance(exc_info.value.__cause__, RoomStateDecodeError)


def test_before_callback_does_not_convert_sniffer_source_failure() -> None:
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            sniffer_messages=_FailingMessageSource(),
            account_state=_AccountState(100001),
        ),
    )

    with pytest.raises(RuntimeError, match="synthetic infrastructure failure"):
        asyncio.run(screen.before_callback())


def test_before_callback_does_not_convert_sniffer_source_timeout() -> None:
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=_TimeoutFailingMessageSource(),
            account_state=_AccountState(100001),
        ),
    )

    with pytest.raises(TimeoutError, match="synthetic infrastructure timeout"):
        asyncio.run(screen.before_callback())

    assert browser.screenshot_count == 0


def test_before_callback_propagates_cancellation() -> None:
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            sniffer_messages=EMPTY_SNIFFER_MESSAGES,
            account_state=_AccountState(100001),
        ),
    )

    async def cancel_before_callback() -> None:
        task = asyncio.create_task(screen.before_callback())
        await asyncio.sleep(0)
        task.cancel()
        with pytest.raises(asyncio.CancelledError):
            await task

    asyncio.run(cancel_before_callback())


def test_wait_for_state_change_returns_newer_cached_state_immediately() -> (
    None
):
    messages = _message_queue(
        _request_response(".lq.Lobby.createRoom", {"room": _room()}),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())
    previous = context.room_state_cache.state
    assert previous is not None
    expected = context.room_state_cache.apply(_ready_notice(), 100001)

    state = asyncio.run(screen.wait_for_state_change(previous))

    assert state is expected
    assert state is not None
    assert state.version == 2


def test_wait_for_state_change_awaits_message_source_without_polling() -> None:
    messages = _QueuedThenWaitingMessageSource(
        _request_response(".lq.Lobby.joinRoom", {"room": _room()}),
        _ready_notice(),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100002),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())
    previous = context.room_state_cache.state
    assert previous is not None

    state = asyncio.run(screen.wait_for_state_change(previous))

    assert state.version == 2
    assert state.players[1].is_ready is True
    assert messages.get_count == 1


@pytest.mark.parametrize(
    ("notice_name", "expected_status"),
    [
        (".lq.NotifyRoomGameStart", RoomStatus.MATCH_STARTED),
        (".lq.NotifyRoomKickOut", RoomStatus.KICKED),
    ],
)
def test_wait_for_state_change_returns_terminal_snapshot_once(
    notice_name: str,
    expected_status: RoomStatus,
) -> None:
    screenshot = b"synthetic-screenshot"
    messages = _QueuedThenWaitingMessageSource(
        _request_response(".lq.Lobby.joinRoom", {"room": _room()}),
        _notice(notice_name),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())
    previous = asyncio.run(screen.get_state())

    state = asyncio.run(screen.wait_for_state_change(previous))

    assert state.version == 2
    assert state.status is expected_status
    with pytest.raises(ScreenStaleError) as exc_info:
        asyncio.run(screen.get_state())
    assert exc_info.value.screenshot == screenshot


def test_wait_for_state_change_cancellation_keeps_applied_snapshot() -> None:
    messages = _UpdateThenBlockingMessageSource(
        _request_response(".lq.Lobby.joinRoom", {"room": _room()}),
        _notice(".lq.Unrelated"),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100002),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())
    previous = asyncio.run(screen.get_state())

    async def wait_with_timeout() -> None:
        async with asyncio.timeout(0.001):
            await screen.wait_for_state_change(previous)

    with pytest.raises(TimeoutError):
        asyncio.run(wait_with_timeout())

    state = asyncio.run(screen.get_state())
    assert state is previous
    assert state.version == 1


@pytest.mark.parametrize(
    "field",
    ["room_id", "self_account_id", "version", "same_version_content"],
)
def test_wait_for_state_change_rejects_mismatched_state(field: str) -> None:
    screenshot = b"synthetic-screenshot"
    messages = _message_queue(
        _request_response(".lq.Lobby.createRoom", {"room": _room()}),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(screenshot),
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())
    current = asyncio.run(screen.get_state())
    if field == "room_id":
        invalid = replace(current, room_id=54321)
    elif field == "self_account_id":
        invalid = replace(current, self_account_id=100002)
    elif field == "version":
        invalid = replace(current, version=current.version + 1)
    else:
        invalid = replace(
            current,
            players=(
                replace(current.players[0], name="changed"),
                *current.players[1:],
            ),
        )

    with pytest.raises(ScreenInvalidArgumentError) as exc_info:
        asyncio.run(screen.wait_for_state_change(invalid))

    assert exc_info.value.screenshot == screenshot


def test_wait_for_state_change_returns_external_host_change() -> None:
    messages = _QueuedThenWaitingMessageSource(
        _request_response(".lq.Lobby.joinRoom", {"room": _room()}),
        _host_change_notice(),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=BrowserControllerSpy(b"synthetic-screenshot"),
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())
    previous = asyncio.run(screen.get_state())

    state = asyncio.run(screen.wait_for_state_change(previous))

    assert state.version == 2
    assert state.self_is_host is True
    assert state.players[0].is_host is False
    assert state.players[1].is_host is True


def test_wait_for_state_change_accepts_keyword_state_and_has_safe_api_log(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _message_queue(
        _request_response(".lq.Lobby.createRoom", {"room": _room()}),
    )
    context = ScreenContext(
        browser=BrowserControllerSpy(b"synthetic-screenshot"),
        sniffer_messages=messages,
        account_state=_AccountState(100001),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())
    previous = asyncio.run(screen.get_state())
    context.room_state_cache.apply(_ready_notice(), 100001)

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        state = asyncio.run(
            screen.wait_for_state_change(state=previous),
        )

    parameters = signature(RoomScreen.wait_for_state_change).parameters
    assert list(parameters) == ["self", "state"]
    assert parameters["state"].kind is Parameter.POSITIONAL_OR_KEYWORD
    assert "timeout" not in parameters
    api_messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert api_messages == [
        "screen API called: screen=RoomScreen api=wait_for_state_change",
    ]
    assert str(state.room_id) not in api_messages[0]
    assert str(state.self_account_id) not in api_messages[0]
    assert all(player.name not in api_messages[0] for player in state.players)
