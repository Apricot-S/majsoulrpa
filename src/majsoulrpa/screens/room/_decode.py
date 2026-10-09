from pydantic import JsonValue

from majsoulrpa.screens._json_fields import (
    JsonFieldDecodeError,
    get_int,
    get_list,
    get_str,
)
from majsoulrpa.screens.room.state import RoomPlayer, RoomState, RoomStatus


class RoomStateDecodeError(ValueError):
    """Raised when a decoded room snapshot violates its wire schema."""


def decode_room_state(
    room: dict[str, JsonValue],
    *,
    version: int,
    self_account_id: int,
) -> RoomState:
    try:
        return _decode_room_state(
            room, version=version, self_account_id=self_account_id
        )
    except JsonFieldDecodeError as error:
        raise RoomStateDecodeError(str(error)) from error


def _decode_room_state(
    room: dict[str, JsonValue],
    *,
    version: int,
    self_account_id: int,
) -> RoomState:
    room_id = _require_positive_int(room, "room_id")
    owner_id = _require_positive_int(room, "owner_id")
    max_player_count = _require_int(room, "max_player_count")
    robots = _require_list(room, "robots")

    ready_list = _require_list(room, "ready_list")
    ready_account_ids = {
        _require_positive_list_int(value, "room.ready_list")
        for value in ready_list
    }

    persons = _require_list(room, "persons")
    players = tuple(
        _decode_room_player(
            value,
            owner_id=owner_id,
            ready_account_ids=ready_account_ids,
        )
        for value in persons
    )
    player_account_ids = {player.account_id for player in players}
    unknown_ready_ids = ready_account_ids - player_account_ids
    if unknown_ready_ids:
        msg = "room.ready_list contains an unknown account ID."
        raise RoomStateDecodeError(msg)

    try:
        return RoomState(
            version=version,
            status=RoomStatus.WAITING,
            room_id=room_id,
            max_player_count=max_player_count,
            players=players,
            ai_count=len(robots),
            self_account_id=self_account_id,
        )
    except ValueError as error:
        raise RoomStateDecodeError(str(error)) from error


def _decode_room_player(
    value: JsonValue,
    *,
    owner_id: int,
    ready_account_ids: set[int],
) -> RoomPlayer:
    if not isinstance(value, dict):
        msg = "room.persons entries must be objects."
        raise RoomStateDecodeError(msg)
    account_id = _require_positive_int(value, "account_id")
    name = get_str(value, "nickname", label="room.persons nickname")
    return RoomPlayer(
        account_id=account_id,
        name=name,
        is_host=account_id == owner_id,
        is_ready=account_id in ready_account_ids,
    )


def _require_list(
    value: dict[str, JsonValue],
    field_name: str,
) -> list[JsonValue]:
    return get_list(value, field_name, label=f"room.{field_name}")


def _require_int(value: dict[str, JsonValue], field_name: str) -> int:
    return get_int(value, field_name, label=f"room.{field_name}")


def _require_positive_int(value: dict[str, JsonValue], field_name: str) -> int:
    result = _require_int(value, field_name)
    if result <= 0:
        msg = f"room.{field_name} must be positive."
        raise RoomStateDecodeError(msg)
    return result


def _require_positive_list_int(value: JsonValue, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        msg = f"{field_name} entries must be positive integers."
        raise RoomStateDecodeError(msg)
    return value
