import datetime as dt
from dataclasses import replace

import pytest
from pydantic import JsonValue

from majsoulrpa.screens.errors import MessageDecodeError
from majsoulrpa.screens.room.store import (
    RoomStateStore,
    RoomStateTransitionError,
)
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    Direction,
    RawNotice,
    RawRequestResponse,
)


def _request_response(
    name: str,
    response: dict[str, JsonValue],
) -> DecodedRequestResponse:
    observed_at = dt.datetime(2026, 1, 2, tzinfo=dt.UTC)
    return DecodedRequestResponse(
        raw=RawRequestResponse(
            request_direction=Direction.OUTBOUND,
            name=name,
            request=b"synthetic-request",
            response=b"synthetic-response",
            request_observed_at=observed_at,
            response_observed_at=observed_at,
        ),
        request={},
        response=response,
    )


def _create_room_message(
    response: dict[str, JsonValue],
) -> DecodedRequestResponse:
    return _request_response(".lq.Lobby.createRoom", response)


def _notice(
    name: str,
    message: dict[str, JsonValue] | None = None,
    *,
    direction: Direction = Direction.INBOUND,
) -> DecodedNotice:
    observed_at = dt.datetime(2026, 1, 2, tzinfo=dt.UTC)
    return DecodedNotice(
        raw=RawNotice(
            direction=direction,
            name=name,
            payload=b"synthetic-notice",
            observed_at=observed_at,
        ),
        message={} if message is None else message,
    )


def _room(
    *,
    room_id: int = 12345,
    ready: bool = False,
) -> dict[str, JsonValue]:
    ready_list: list[JsonValue] = [100002] if ready else []
    return {
        "room_id": room_id,
        "owner_id": 100001,
        "max_player_count": 4,
        "persons": [
            {"account_id": 100001, "nickname": "host"},
            {"account_id": 100002, "nickname": "guest"},
        ],
        "ready_list": ready_list,
        "robot_count": 0,
        "robots": [],
    }


def test_store_applies_created_room_as_initial_state() -> None:
    cache = RoomStateStore()
    assert cache.state is None

    state = cache.apply(
        _create_room_message(
            {
                "room": {
                    "room_id": 12345,
                    "owner_id": 100001,
                    "max_player_count": 4,
                    "persons": [
                        {"account_id": 100001, "nickname": "host"},
                    ],
                    "ready_list": [],
                    "robot_count": 0,
                    "robots": [],
                },
            },
        ),
        100001,
    )

    assert state is cache.state
    assert state is not None
    assert state.version == 1
    assert state.room_id == 12345
    assert state.self_is_host is True


def test_store_does_not_increment_version_for_identical_snapshot() -> None:
    cache = RoomStateStore()
    message = _create_room_message(
        {
            "room": {
                "room_id": 12345,
                "owner_id": 100001,
                "max_player_count": 4,
                "persons": [
                    {"account_id": 100001, "nickname": "host"},
                ],
                "ready_list": [],
                "robot_count": 0,
                "robots": [],
            },
        },
    )
    first = cache.apply(message, 100001)

    second = cache.apply(message, 100001)

    assert second is first
    assert second is not None
    assert second.version == 1


@pytest.mark.parametrize(
    "name",
    [".lq.Lobby.joinRoom", ".lq.Lobby.fetchRoom"],
)
def test_store_accepts_other_complete_room_snapshots(name: str) -> None:
    cache = RoomStateStore()

    state = cache.apply(
        _request_response(name, {"room": _room()}),
        100002,
    )

    assert state is not None
    assert state.version == 1
    assert state.room_id == 12345


@pytest.mark.parametrize(
    "name",
    [
        ".lq.Lobby.createRoom",
        ".lq.Lobby.joinRoom",
        ".lq.Lobby.fetchRoom",
    ],
)
def test_store_does_not_initialize_from_failed_response(name: str) -> None:
    cache = RoomStateStore()

    state = cache.apply(
        _request_response(name, {"error": {"code": 9999}}),
        100001,
    )

    assert state is None
    assert cache.state is None


def test_store_increments_version_for_changed_snapshot() -> None:
    cache = RoomStateStore()
    cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    state = cache.apply(
        _request_response(
            ".lq.Lobby.fetchRoom",
            {"room": _room(ready=True)},
        ),
        100002,
    )

    assert state is not None
    assert state.version == 2
    assert state.players[1].is_ready is True


def test_store_rejects_different_room_while_active() -> None:
    cache = RoomStateStore()
    cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    with pytest.raises(RoomStateTransitionError):
        cache.apply(
            _request_response(
                ".lq.Lobby.fetchRoom",
                {"room": _room(room_id=54321)},
            ),
            100002,
        )


def test_store_rejects_reinitialization_after_game_start() -> None:
    cache = RoomStateStore()
    cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    terminal = cache.apply(
        _notice(".lq.NotifyRoomGameStart"),
        100002,
    )
    assert terminal is not None
    assert terminal.status.value == "match_started"
    assert terminal.version == 2
    with pytest.raises(
        RoomStateTransitionError,
        match="cannot be reinitialized",
    ):
        cache.apply(
            _request_response(
                ".lq.Lobby.joinRoom",
                {"room": _room(room_id=54321)},
            ),
            100002,
        )


def test_store_marks_successful_leave_as_terminal() -> None:
    cache = RoomStateStore()
    initial = cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    terminal = cache.apply(
        _request_response(".lq.Lobby.leaveRoom", {}),
        100002,
    )

    assert initial is not None
    assert terminal is not None
    assert terminal.status.value == "left"
    assert terminal.version == 2
    assert terminal.room_id == initial.room_id
    assert terminal.players == initial.players


def test_store_keeps_waiting_state_after_rejected_leave() -> None:
    cache = RoomStateStore()
    initial = cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    state = cache.apply(
        _request_response(
            ".lq.Lobby.leaveRoom",
            {"error": {"code": 9999}},
        ),
        100002,
    )

    assert state is initial
    assert state is not None
    assert state.status.value == "waiting"
    assert state.version == 1


@pytest.mark.parametrize(
    "name",
    [
        ".lq.Lobby.createRoom",
        ".lq.Lobby.joinRoom",
        ".lq.Lobby.fetchRoom",
        ".lq.Lobby.leaveRoom",
    ],
)
@pytest.mark.parametrize("state", ["uninitialized", "active", "terminal"])
@pytest.mark.parametrize(
    "rejected", [False, True], ids=["success", "rejection"]
)
def test_store_rejects_inbound_room_requests_without_state_change(
    name: str,
    state: str,
    *,
    rejected: bool,
) -> None:
    store = RoomStateStore()
    if state != "uninitialized":
        store.apply(_create_room_message({"room": _room()}), 100002)
    if state == "terminal":
        store.apply(_notice(".lq.NotifyRoomKickOut"), 100002)
    previous = store.state
    response: dict[str, JsonValue] = (
        {"error": {"code": 9999}} if rejected else {"room": _room(ready=True)}
    )
    message = _request_response(name, response)
    message = replace(
        message,
        raw=replace(message.raw, request_direction=Direction.INBOUND),
    )

    with pytest.raises(RoomStateTransitionError, match="outbound request"):
        store.apply(message, 100002)

    assert store.state is previous


@pytest.mark.parametrize(
    "name", [".lq.NotifyRoomGameStart", ".lq.NotifyRoomKickOut"]
)
@pytest.mark.parametrize("state", ["uninitialized", "active", "terminal"])
def test_store_rejects_outbound_terminal_notices_without_state_change(
    name: str,
    state: str,
) -> None:
    store = RoomStateStore()
    if state != "uninitialized":
        store.apply(_create_room_message({"room": _room()}), 100002)
    if state == "terminal":
        store.apply(_notice(".lq.NotifyRoomKickOut"), 100002)
    previous = store.state

    with pytest.raises(RoomStateTransitionError, match="inbound notice"):
        store.apply(_notice(name, direction=Direction.OUTBOUND), 100002)

    assert store.state is previous


def test_store_marks_kick_notice_as_terminal() -> None:
    cache = RoomStateStore()
    initial = cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    terminal = cache.apply(
        _notice(".lq.NotifyRoomKickOut"),
        100002,
    )

    assert initial is not None
    assert terminal is not None
    assert terminal.status.value == "kicked"
    assert terminal.version == 2
    assert terminal.room_id == initial.room_id
    assert terminal.players == initial.players


def test_store_applies_player_update_and_rederives_host() -> None:
    cache = RoomStateStore()
    cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    state = cache.apply(
        _notice(
            ".lq.NotifyRoomPlayerUpdate",
            {
                "owner_id": 100002,
                "robot_count": 0,
                "player_list": [
                    {"account_id": 100001, "nickname": "former-host"},
                    {"account_id": 100002, "nickname": "new-host"},
                ],
                "robots": [{"account_id": 0, "nickname": "synthetic-ai"}],
                "positions": [],
            },
        ),
        100002,
    )

    assert state is not None
    assert state.version == 2
    assert state.self_is_host is True
    assert state.players[0].is_host is False
    assert state.players[1].is_host is True
    assert state.ai_count == 1


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("player_list", None),
        ("player_list", [None]),
        ("player_list", [{"account_id": True, "nickname": "synthetic"}]),
        ("player_list", [{"account_id": 0, "nickname": "synthetic"}]),
        ("player_list", [{"account_id": 100001, "nickname": None}]),
        ("player_list", [{"account_id": 100001, "nickname": "synthetic"}]),
        ("owner_id", 999999),
        ("robots", None),
        ("robots", [{}, {}, {}]),
    ],
    ids=[
        "not-list",
        "not-object",
        "boolean-id",
        "nonpositive-id",
        "invalid-name",
        "missing-self",
        "missing-owner",
        "invalid-robots",
        "too-many-participants",
    ],
)
def test_player_update_rejects_invalid_data_without_state_change(
    field: str,
    value: JsonValue,
) -> None:
    store = RoomStateStore()
    initial = store.apply(
        _create_room_message({"room": _room(ready=True)}), 100002
    )
    room = _room()
    update: dict[str, JsonValue] = {
        "owner_id": room["owner_id"],
        "player_list": room["persons"],
        "robots": room["robots"],
    }
    update[field] = value

    with pytest.raises(MessageDecodeError):
        store.apply(_notice(".lq.NotifyRoomPlayerUpdate", update), 100002)

    assert store.state is initial


def test_player_update_preserves_ready_only_for_existing_players() -> None:
    store = RoomStateStore()
    initial = store.apply(
        _create_room_message({"room": _room(ready=True)}), 100002
    )
    update: dict[str, JsonValue] = {
        "owner_id": 100001,
        "player_list": [
            {"account_id": 100001, "nickname": "host"},
            {"account_id": 100002, "nickname": "guest"},
            {"account_id": 100003, "nickname": "new-guest"},
        ],
        "robots": [],
    }
    message = _notice(".lq.NotifyRoomPlayerUpdate", update)

    state = store.apply(message, 100002)

    assert initial is not None
    assert state is not None
    assert state.version == initial.version + 1
    assert [player.is_ready for player in state.players] == [
        False,
        True,
        False,
    ]
    assert len(initial.players) == 2
    assert initial.self_is_ready is True
    assert store.apply(message, 100002) is state


@pytest.mark.parametrize(
    "payload",
    [
        {"ready": True},
        {"account_id": None, "ready": True},
        {"account_id": True, "ready": True},
        {"account_id": "100002", "ready": True},
        {"account_id": 0, "ready": True},
        {"account_id": -1, "ready": True},
        {"account_id": 999999, "ready": True},
        {"account_id": 100002},
        {"account_id": 100002, "ready": None},
        {"account_id": 100002, "ready": 1},
        {"account_id": 100002, "ready": "true"},
    ],
    ids=[
        "missing-id",
        "null-id",
        "boolean-id",
        "string-id",
        "zero-id",
        "negative-id",
        "unknown-id",
        "missing-ready",
        "null-ready",
        "integer-ready",
        "string-ready",
    ],
)
def test_ready_update_rejects_invalid_data_without_state_change(
    payload: dict[str, JsonValue],
) -> None:
    store = RoomStateStore()
    initial = store.apply(_create_room_message({"room": _room()}), 100002)

    with pytest.raises(MessageDecodeError):
        store.apply(_notice(".lq.NotifyRoomPlayerReady", payload), 100002)

    assert store.state is initial


def test_ready_update_ignores_invalid_old_notice_after_terminal() -> None:
    store = RoomStateStore()
    store.apply(_create_room_message({"room": _room()}), 100002)
    terminal = store.apply(_notice(".lq.NotifyRoomKickOut"), 100002)

    assert (
        store.apply(_notice(".lq.NotifyRoomPlayerReady"), 100002) is terminal
    )


@pytest.mark.parametrize("ready", [True, False], ids=["set", "clear"])
def test_store_applies_ready_notice_to_target_player(*, ready: bool) -> None:
    cache = RoomStateStore()
    initial = cache.apply(
        _create_room_message({"room": _room(ready=not ready)}),
        100002,
    )

    state = cache.apply(
        _notice(
            ".lq.NotifyRoomPlayerReady",
            {"account_id": 100002, "ready": ready},
        ),
        100002,
    )

    assert state is not None
    assert state.version == 2
    assert state.players[0].is_ready is False
    assert state.players[1].is_ready is ready
    assert initial is not None
    assert initial.self_is_ready is not ready
    assert (
        cache.apply(
            _notice(
                ".lq.NotifyRoomPlayerReady",
                {"account_id": 100002, "ready": ready},
            ),
            100002,
        )
        is state
    )


@pytest.mark.parametrize(
    "name",
    [
        ".lq.NotifyRoomPlayerUpdate",
        ".lq.NotifyRoomPlayerReady",
    ],
)
def test_store_rejects_outbound_player_notice(name: str) -> None:
    cache = RoomStateStore()
    initial = cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    with pytest.raises(RoomStateTransitionError, match="inbound"):
        cache.apply(
            _notice(name, direction=Direction.OUTBOUND),
            100002,
        )

    assert cache.state is initial


def test_player_update_drops_ready_state_for_player_who_left() -> None:
    cache = RoomStateStore()
    room = _room()
    room["persons"] = [
        {"account_id": 100001, "nickname": "host"},
        {"account_id": 100002, "nickname": "self"},
        {"account_id": 100003, "nickname": "leaving-player"},
    ]
    room["ready_list"] = [100003]
    cache.apply(
        _create_room_message({"room": room}),
        100002,
    )

    state = cache.apply(
        _notice(
            ".lq.NotifyRoomPlayerUpdate",
            {
                "owner_id": 100001,
                "robot_count": 0,
                "player_list": [
                    {"account_id": 100001, "nickname": "host"},
                    {"account_id": 100002, "nickname": "self"},
                ],
                "robots": [],
                "positions": [],
            },
        ),
        100002,
    )

    assert state is not None
    assert state.version == 2
    assert [player.account_id for player in state.players] == [100001, 100002]
    assert all(not player.is_ready for player in state.players)


def test_store_ignores_old_room_update_after_terminal_state() -> None:
    cache = RoomStateStore()
    cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )
    terminal = cache.apply(
        _notice(".lq.NotifyRoomKickOut"),
        100002,
    )

    state = cache.apply(
        _notice(
            ".lq.NotifyRoomPlayerUpdate",
            {
                "owner_id": 100002,
                "robot_count": 1,
                "player_list": [
                    {"account_id": 100002, "nickname": "stale-update"},
                ],
                "robots": [],
                "positions": [],
            },
        ),
        100002,
    )

    assert state is terminal
    assert state is not None
    assert state.status.value == "kicked"
    assert state.version == 2
