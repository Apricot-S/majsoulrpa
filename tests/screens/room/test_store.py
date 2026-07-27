import datetime
from dataclasses import replace

import pytest
from pydantic import JsonValue

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
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
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
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
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


def test_store_requires_leave_request_to_be_outbound() -> None:
    cache = RoomStateStore()
    cache.apply(_create_room_message({"room": _room()}), 100002)
    message = _request_response(".lq.Lobby.leaveRoom", {})
    message = replace(
        message,
        raw=replace(message.raw, request_direction=Direction.INBOUND),
    )

    with pytest.raises(RoomStateTransitionError):
        cache.apply(message, 100002)


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


def test_store_applies_ready_notice_to_target_player() -> None:
    cache = RoomStateStore()
    cache.apply(
        _create_room_message({"room": _room()}),
        100002,
    )

    state = cache.apply(
        _notice(
            ".lq.NotifyRoomPlayerReady",
            {"account_id": 100002, "ready": True},
        ),
        100002,
    )

    assert state is not None
    assert state.version == 2
    assert state.players[0].is_ready is False
    assert state.players[1].is_ready is True


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
