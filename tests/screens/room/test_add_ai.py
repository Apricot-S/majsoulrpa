import asyncio
import logging
from dataclasses import replace
from inspect import signature

import pytest
from pydantic import JsonValue

from majsoulrpa.assets.templates.room import (
    ADD_AI_SETTINGS_PATHS,
    ADD_AI_TEMPLATE_PATH,
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
    RoomState,
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
    _synthetic_templates_screenshot,
)
from tests.screens.room.test_leave import _OperationMessageSource
from tests.screens.room.test_state_api import _AccountState, _notice, _room


def _player_update(
    *,
    owner_id: int = 100001,
    ai_count: int = 1,
) -> DecodedNotice:
    return _notice(
        ".lq.NotifyRoomPlayerUpdate",
        {
            "owner_id": owner_id,
            "robot_count": 0,
            "player_list": [
                {"account_id": 100001, "nickname": "host"},
                {"account_id": 100002, "nickname": "guest"},
            ],
            "robots": [{}] * ai_count,
            "positions": [],
        },
    )


@pytest.mark.parametrize("position", range(4))
def test_add_ai_clicks_detected_position_and_waits_for_player_update(
    position: int,
) -> None:
    update = _player_update()
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(
            _request_response(".lq.Lobby.addRoomRobot", {}),
            update,
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[position],
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

    state = asyncio.run(screen.add_ai())

    assert len(browser.clicked_points) == 1
    assert messages.get_count == 2
    assert state.version == 2
    assert state.ai_count == 1


def test_add_ai_accepts_player_update_before_response() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(
            _player_update(),
            _request_response(".lq.Lobby.addRoomRobot", {}),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[0],
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

    async def add_ai() -> RoomState:
        async with asyncio.timeout(0.01):
            return await screen.add_ai()

    state = asyncio.run(add_ai())

    assert state.ai_count == 1
    assert messages.get_count == 2


@pytest.mark.parametrize(
    ("self_account_id", "ai_count", "expected_reason"),
    [
        (100002, 0, RoomOperationNotAllowedReason.NOT_HOST),
        (100001, 2, RoomOperationNotAllowedReason.ROOM_FULL),
    ],
)
def test_add_ai_rejects_failed_precondition_without_clicking(
    self_account_id: int,
    ai_count: int,
    expected_reason: RoomOperationNotAllowedReason,
) -> None:
    room = _room()
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
        asyncio.run(screen.add_ai())

    assert exc_info.value.operation is RoomOperation.ADD_AI
    assert exc_info.value.reason is expected_reason
    assert browser.clicked_points == []
    assert messages.get_count == 0


def test_add_ai_uses_latest_host_state_before_clicking() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
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
    messages.enqueue(_player_update(owner_id=100002, ai_count=0))

    with pytest.raises(RoomOperationNotAllowedError) as exc_info:
        asyncio.run(screen.add_ai())

    assert exc_info.value.reason is RoomOperationNotAllowedReason.NOT_HOST
    assert browser.clicked_points == []


def test_add_ai_server_rejection_keeps_screen_active() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(
            _request_response(
                ".lq.Lobby.addRoomRobot",
                {"error": {"code": 9999, "message": "sensitive"}},
            ),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[0],
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
        asyncio.run(screen.add_ai())

    error = exc_info.value
    assert error.operation is RoomOperation.ADD_AI
    assert error.reason is RoomOperationFailureReason.UNRECOGNIZED_ERROR_CODE
    assert error.server_error_code == 9999
    assert "sensitive" not in str(error)
    assert asyncio.run(screen.get_state()).ai_count == 0


@pytest.mark.parametrize(
    "waiting",
    [
        (_request_response(".lq.Lobby.addRoomRobot", {}),),
        (
            _request_response(".lq.Lobby.addRoomRobot", {}),
            _player_update(ai_count=2),
        ),
        (_player_update(),),
    ],
)
def test_add_ai_waits_for_subsequent_single_ai_update(
    waiting: tuple[DecodedSnifferMessage, ...],
) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=waiting,
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[0],
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

    async def add_ai_with_timeout() -> None:
        async with asyncio.timeout(0.001):
            await screen.add_ai()

    with pytest.raises(TimeoutError):
        asyncio.run(add_ai_with_timeout())

    assert len(browser.clicked_points) == 1
    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


@pytest.mark.parametrize(
    "error",
    [None, {}, {"code": True}, {"code": "invalid"}],
)
def test_add_ai_rejects_malformed_server_error(error: JsonValue) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(
            _request_response(".lq.Lobby.addRoomRobot", {"error": error}),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[0],
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
        asyncio.run(screen.add_ai())


def test_add_ai_requires_outbound_request_response() -> None:
    response = _request_response(".lq.Lobby.addRoomRobot", {})
    response = replace(
        response,
        raw=replace(response.raw, request_direction=Direction.INBOUND),
    )
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(response,),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[0],
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
        asyncio.run(screen.add_ai())


def test_add_ai_requires_detectable_button() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
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
        asyncio.run(screen.add_ai())

    assert browser.clicked_points == []
    assert messages.get_count == 0


def test_add_ai_clicks_only_one_button_when_multiple_are_visible() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(
            _request_response(".lq.Lobby.addRoomRobot", {}),
            _player_update(),
        ),
    )
    screenshot = _synthetic_templates_screenshot(
        tuple(
            (ADD_AI_TEMPLATE_PATH, settings_path)
            for settings_path in ADD_AI_SETTINGS_PATHS
        ),
    )
    browser = BrowserControllerSpy(screenshot)
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100001),
        ),
    )
    asyncio.run(screen.before_callback())

    asyncio.run(screen.add_ai())

    assert len(browser.clicked_points) == 1


def test_kick_interrupts_add_ai_wait() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(_notice(".lq.NotifyRoomKickOut"),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[0],
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
        asyncio.run(screen.add_ai())

    assert screen._room_state_store.state is not None
    assert screen._room_state_store.state.status is RoomStatus.KICKED


def test_add_ai_has_no_timeout_argument_and_safe_api_log(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.createRoom", {"room": _room()}),),
        waiting=(
            _request_response(".lq.Lobby.addRoomRobot", {}),
            _player_update(),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=ADD_AI_TEMPLATE_PATH,
            settings_path=ADD_AI_SETTINGS_PATHS[0],
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
        state = asyncio.run(screen.add_ai())

    assert list(signature(RoomScreen.add_ai).parameters) == ["self"]
    api_messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert api_messages == ["screen API called: screen=RoomScreen api=add_ai"]
    assert str(state.room_id) not in api_messages[0]
