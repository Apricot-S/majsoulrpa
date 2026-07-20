from dataclasses import FrozenInstanceError, replace

import pytest
from pydantic import JsonValue

from majsoulrpa.screens.room._decode import (
    RoomStateDecodeError,
    decode_room_state,
)
from majsoulrpa.screens.room.state import (
    RoomPlayer,
    RoomState,
    RoomStatus,
)


def _room() -> dict[str, JsonValue]:
    return {
        "room_id": 12345,
        "owner_id": 100001,
        "max_player_count": 4,
        "persons": [
            {"account_id": 100001, "nickname": "host"},
            {"account_id": 100002, "nickname": "guest"},
        ],
        "ready_list": [100002],
        "robot_count": 0,
        "robots": [{"account_id": 0, "nickname": "synthetic-ai"}],
    }


def test_decode_waiting_room_state() -> None:
    state = decode_room_state(
        _room(),
        version=1,
        self_account_id=100002,
    )

    assert state == RoomState(
        version=1,
        status=RoomStatus.WAITING,
        room_id=12345,
        max_player_count=4,
        players=(
            RoomPlayer(
                account_id=100001,
                name="host",
                is_host=True,
                is_ready=False,
            ),
            RoomPlayer(
                account_id=100002,
                name="guest",
                is_host=False,
                is_ready=True,
            ),
        ),
        ai_count=1,
        self_account_id=100002,
    )
    assert state.self_is_host is False
    assert state.self_is_ready is True
    assert state.all_guests_ready is True
    assert state.participant_count == 3
    assert state.available_slots == 1
    with pytest.raises(FrozenInstanceError):
        state.ai_count = 2  # ty: ignore[invalid-assignment]


def test_all_guests_ready_is_false_when_any_guest_is_not_ready() -> None:
    room = _room()
    room["persons"] = [
        {"account_id": 100001, "nickname": "host"},
        {"account_id": 100002, "nickname": "ready-guest"},
        {"account_id": 100003, "nickname": "unready-guest"},
    ]
    room["robots"] = []

    state = decode_room_state(
        room,
        version=1,
        self_account_id=100001,
    )

    assert state.all_guests_ready is False


def test_all_guests_ready_is_true_without_human_guests() -> None:
    room = _room()
    room["persons"] = [
        {"account_id": 100001, "nickname": "host"},
    ]
    room["ready_list"] = []
    room["robots"] = [{}, {}, {}]

    state = decode_room_state(
        room,
        version=1,
        self_account_id=100001,
    )

    assert state.all_guests_ready is True


def test_decode_vs_ai_room_state_with_host_as_only_participant() -> None:
    room = _room()
    room["max_player_count"] = 1
    room["persons"] = [
        {"account_id": 100001, "nickname": "host"},
    ]
    room["ready_list"] = []
    room["robots"] = []

    state = decode_room_state(
        room,
        version=1,
        self_account_id=100001,
    )

    assert state.max_player_count == 1
    assert state.participant_count == 1
    assert state.available_slots == 0
    assert state.all_guests_ready is True


def test_room_player_rejects_non_positive_account_id() -> None:
    with pytest.raises(ValueError, match="account ID must be positive"):
        RoomPlayer(
            account_id=0,
            name="synthetic-player",
            is_host=True,
            is_ready=False,
        )


@pytest.mark.parametrize(
    ("field_name", "value"),
    [
        ("room_id", 0),
        ("room_id", True),
        ("owner_id", 0),
        ("owner_id", True),
        ("max_player_count", 2),
        ("max_player_count", True),
    ],
)
def test_decode_rejects_invalid_room_numbers(
    field_name: str,
    value: int,
) -> None:
    room = _room()
    room[field_name] = value

    with pytest.raises(RoomStateDecodeError):
        decode_room_state(room, version=1, self_account_id=100002)


def test_decode_rejects_non_list_robots() -> None:
    room = _room()
    room["robots"] = None

    with pytest.raises(RoomStateDecodeError):
        decode_room_state(room, version=1, self_account_id=100002)


@pytest.mark.parametrize(
    "persons",
    [
        [
            {"account_id": 100001, "nickname": "host"},
            {"account_id": 100001, "nickname": "duplicate"},
        ],
        [{"account_id": 100002, "nickname": "guest"}],
        [{"account_id": True, "nickname": "invalid"}],
    ],
)
def test_decode_rejects_duplicate_or_missing_owner(
    persons: list[JsonValue],
) -> None:
    room = _room()
    room["persons"] = persons

    with pytest.raises(RoomStateDecodeError):
        decode_room_state(room, version=1, self_account_id=100002)


def test_decode_rejects_self_account_id_outside_room() -> None:
    with pytest.raises(RoomStateDecodeError):
        decode_room_state(_room(), version=1, self_account_id=999999)


def test_decode_rejects_ready_account_id_outside_room() -> None:
    room = _room()
    room["ready_list"] = [999999]

    with pytest.raises(RoomStateDecodeError):
        decode_room_state(room, version=1, self_account_id=100002)


def test_decode_rejects_participant_count_over_capacity() -> None:
    room = _room()
    room["max_player_count"] = 3
    room["robots"] = [{}, {}]

    with pytest.raises(RoomStateDecodeError):
        decode_room_state(room, version=1, self_account_id=100002)


@pytest.mark.parametrize(
    "status",
    [RoomStatus.MATCH_STARTED, RoomStatus.LEFT, RoomStatus.KICKED],
)
def test_terminal_state_keeps_last_room_information(
    status: RoomStatus,
) -> None:
    waiting = decode_room_state(
        _room(),
        version=1,
        self_account_id=100002,
    )

    terminal = replace(waiting, version=2, status=status)

    assert terminal.room_id == waiting.room_id
    assert terminal.max_player_count == waiting.max_player_count
    assert terminal.players == waiting.players
    assert terminal.ai_count == waiting.ai_count
    assert terminal.self_account_id == waiting.self_account_id


@pytest.mark.parametrize("max_player_count", [2, True, 1.0])
def test_room_state_rejects_invalid_max_player_count(
    max_player_count: int,
) -> None:
    with pytest.raises(ValueError, match="maximum player count"):
        RoomState(
            version=1,
            status=RoomStatus.WAITING,
            room_id=12345,
            max_player_count=max_player_count,
            players=(
                RoomPlayer(100001, "host", is_host=True, is_ready=False),
            ),
            ai_count=0,
            self_account_id=100001,
        )
