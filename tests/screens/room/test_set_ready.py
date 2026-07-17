import asyncio
import logging
from dataclasses import replace
from importlib.resources.abc import Traversable
from inspect import Parameter, signature

import pytest
from pydantic import JsonValue

from majsoulrpa.assets.templates.room import (
    CANCEL_SETTINGS_PATH,
    CANCEL_TEMPLATE_PATH,
    READY_SETTINGS_PATH,
    READY_TEMPLATE_PATH,
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
    DecodedRequestResponse,
    Direction,
)
from tests.screens.home._support import (
    BrowserControllerSpy,
    _request_response,
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)
from tests.screens.room.test_leave import _OperationMessageSource
from tests.screens.room.test_state_api import _AccountState, _notice, _room


def _ready_response(*, ready: bool) -> DecodedRequestResponse:
    return replace(
        _request_response(".lq.Lobby.readyPlay", {}),
        request={"ready": ready},
    )


def _ready_notice(*, ready: bool, account_id: int = 100002) -> DecodedNotice:
    return _notice(
        ".lq.NotifyRoomPlayerReady",
        {"account_id": account_id, "ready": ready},
    )


@pytest.mark.parametrize(
    ("ready", "template_path", "settings_path"),
    [
        (True, READY_TEMPLATE_PATH, READY_SETTINGS_PATH),
        (False, CANCEL_TEMPLATE_PATH, CANCEL_SETTINGS_PATH),
    ],
)
def test_set_ready_clicks_target_button_and_waits_for_own_ready_notice(
    ready: bool,  # noqa: FBT001
    template_path: Traversable,
    settings_path: Traversable,
) -> None:
    room = _room()
    room["ready_list"] = [] if ready else [100002]
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": room}),),
        waiting=(
            _ready_response(ready=ready),
            _ready_notice(ready=ready),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=template_path,
            settings_path=settings_path,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    state = asyncio.run(screen.set_ready(ready=ready))

    self_player = next(
        player
        for player in state.players
        if player.account_id == state.self_account_id
    )
    assert self_player.is_ready is ready
    assert len(browser.clicked_points) == 1
    assert messages.get_count == 2


@pytest.mark.parametrize("ready", [True, False])
def test_set_ready_returns_same_snapshot_when_already_in_target_state(
    ready: bool,  # noqa: FBT001
) -> None:
    room = _room()
    room["ready_list"] = [100002] if ready else []
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": room}),),
        waiting=(),
    )
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())
    previous = asyncio.run(screen.get_state())

    state = asyncio.run(screen.set_ready(ready=ready))

    assert state is previous
    assert browser.clicked_points == []
    assert messages.get_count == 0


@pytest.mark.parametrize("ready", [True, False])
def test_set_ready_rejects_host_without_clicking(
    ready: bool,  # noqa: FBT001
) -> None:
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

    with pytest.raises(RoomOperationNotAllowedError) as exc_info:
        asyncio.run(screen.set_ready(ready=ready))

    assert exc_info.value.operation is RoomOperation.SET_READY
    assert exc_info.value.reason is RoomOperationNotAllowedReason.NOT_GUEST
    assert browser.clicked_points == []
    assert messages.get_count == 0


def test_set_ready_accepts_own_ready_notice_before_response() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_ready_notice(ready=True), _ready_response(ready=True)),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    state = asyncio.run(screen.set_ready())

    assert next(
        player.is_ready
        for player in state.players
        if player.account_id == state.self_account_id
    )
    assert messages.get_count == 2


def test_set_ready_rejects_request_for_different_target_state() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_ready_response(ready=False),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.set_ready())

    assert len(browser.clicked_points) == 1


def test_set_ready_server_rejection_keeps_screen_active() -> None:
    response = replace(
        _request_response(
            ".lq.Lobby.readyPlay",
            {"error": {"code": 9999, "message": "sensitive"}},
        ),
        request={"ready": True},
    )
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(response,),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(RoomOperationRejectedError) as exc_info:
        asyncio.run(screen.set_ready())

    error = exc_info.value
    assert error.operation is RoomOperation.SET_READY
    assert error.reason is RoomOperationFailureReason.UNRECOGNIZED_ERROR_CODE
    assert error.server_error_code == 9999
    assert "sensitive" not in str(error)
    assert asyncio.run(screen.get_state()).status == "waiting"


@pytest.mark.parametrize(
    "waiting",
    [
        (_ready_response(ready=True),),
        (_ready_notice(ready=True),),
        (
            _ready_response(ready=True),
            _ready_notice(ready=True, account_id=100001),
        ),
        (_ready_response(ready=True), _ready_notice(ready=False)),
    ],
)
def test_set_ready_waits_for_response_and_matching_own_notice(
    waiting: tuple[DecodedRequestResponse | DecodedNotice, ...],
) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=waiting,
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    async def set_ready_with_timeout() -> None:
        async with asyncio.timeout(0.001):
            await screen.set_ready()

    with pytest.raises(TimeoutError):
        asyncio.run(set_ready_with_timeout())

    assert len(browser.clicked_points) == 1
    assert asyncio.run(screen.get_state()).status == "waiting"


def test_set_ready_does_not_return_after_target_state_is_reverted() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(
            _ready_notice(ready=True),
            _ready_notice(ready=False),
            _ready_response(ready=True),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    async def set_ready_with_timeout() -> None:
        async with asyncio.timeout(0.001):
            await screen.set_ready()

    with pytest.raises(TimeoutError):
        asyncio.run(set_ready_with_timeout())

    state = asyncio.run(screen.get_state())
    assert not next(
        player.is_ready
        for player in state.players
        if player.account_id == state.self_account_id
    )


def test_set_ready_preserves_matching_notice_across_other_player_notice() -> (
    None
):
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(
            _ready_notice(ready=True),
            _ready_notice(ready=True, account_id=100001),
            _ready_response(ready=True),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    async def set_ready_with_timeout() -> RoomState:
        async with asyncio.timeout(0.01):
            return await screen.set_ready()

    state = asyncio.run(set_ready_with_timeout())

    assert next(
        player.is_ready
        for player in state.players
        if player.account_id == state.self_account_id
    )


def test_set_ready_uses_latest_host_state_before_clicking() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(),
    )
    browser = BrowserControllerSpy(b"synthetic-screenshot")
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())
    messages.enqueue(
        _notice(
            ".lq.NotifyRoomPlayerUpdate",
            {
                "owner_id": 100002,
                "player_list": [
                    {"account_id": 100001, "nickname": "former-host"},
                    {"account_id": 100002, "nickname": "self"},
                ],
                "robots": [],
                "positions": [],
            },
        ),
    )

    with pytest.raises(RoomOperationNotAllowedError) as exc_info:
        asyncio.run(screen.set_ready())

    assert exc_info.value.reason is RoomOperationNotAllowedReason.NOT_GUEST
    assert browser.clicked_points == []
    assert messages.get_count == 0


def test_set_ready_does_not_use_historical_ready_response() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(
            _ready_response(ready=True),
            _ready_notice(ready=True),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())
    messages.enqueue(_ready_response(ready=True))

    state = asyncio.run(screen.set_ready())

    assert next(
        player.is_ready
        for player in state.players
        if player.account_id == state.self_account_id
    )
    assert len(browser.clicked_points) == 1
    assert messages.get_count == 2


def test_set_ready_requires_target_template() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(),
    )
    browser = BrowserControllerSpy(_synthetic_blank_screenshot())
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenDetectionError):
        asyncio.run(screen.set_ready())

    assert browser.clicked_points == []
    assert messages.get_count == 0


def test_kick_interrupts_set_ready_wait() -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(_notice(".lq.NotifyRoomKickOut"),),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    context = ScreenContext(
        browser=browser,
        sniffer_messages=messages,
        account_state=_AccountState(100002),
    )
    screen = RoomScreen(context=context)
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenStaleError):
        asyncio.run(screen.set_ready())

    assert len(browser.clicked_points) == 1
    assert context.room_state_cache.state is not None
    assert context.room_state_cache.state.status is RoomStatus.KICKED


@pytest.mark.parametrize(
    "error",
    [None, {}, {"code": True}, {"code": "invalid"}],
)
def test_set_ready_rejects_malformed_server_error(error: JsonValue) -> None:
    response = replace(
        _request_response(".lq.Lobby.readyPlay", {"error": error}),
        request={"ready": True},
    )
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(response,),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.set_ready())

    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_set_ready_requires_outbound_request_response() -> None:
    response = _ready_response(ready=True)
    response = replace(
        response,
        raw=replace(response.raw, request_direction=Direction.INBOUND),
    )
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(response,),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    with pytest.raises(ScreenInconsistentMessageError):
        asyncio.run(screen.set_ready())

    assert asyncio.run(screen.get_state()).status is RoomStatus.WAITING


def test_set_ready_has_keyword_only_target_and_safe_api_log(
    caplog: pytest.LogCaptureFixture,
) -> None:
    messages = _OperationMessageSource(
        queued=(_request_response(".lq.Lobby.joinRoom", {"room": _room()}),),
        waiting=(
            _ready_response(ready=True),
            _ready_notice(ready=True),
        ),
    )
    browser = BrowserControllerSpy(
        _synthetic_template_screenshot(
            template_path=READY_TEMPLATE_PATH,
            settings_path=READY_SETTINGS_PATH,
        ),
    )
    screen = RoomScreen(
        context=ScreenContext(
            browser=browser,
            sniffer_messages=messages,
            account_state=_AccountState(100002),
        ),
    )
    asyncio.run(screen.before_callback())

    with caplog.at_level(logging.INFO, logger="majsoulrpa.screens.api"):
        asyncio.run(screen.set_ready())

    parameters = signature(RoomScreen.set_ready).parameters
    assert list(parameters) == ["self", "ready"]
    assert parameters["ready"].kind is Parameter.KEYWORD_ONLY
    assert parameters["ready"].default is True
    api_messages = [
        record.getMessage()
        for record in caplog.records
        if record.name == "majsoulrpa.screens.api"
    ]
    assert api_messages == [
        "screen API called: screen=RoomScreen api=set_ready",
    ]
