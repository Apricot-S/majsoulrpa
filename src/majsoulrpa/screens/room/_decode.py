from pydantic import JsonValue

from majsoulrpa.screens.room.state import RoomPlayer, RoomState, RoomStatus


class RoomStateDecodeError(ValueError):
    """Raised when a decoded room snapshot violates its wire schema."""


def decode_room_state(
    room: dict[str, JsonValue],
    *,
    version: int,
    self_account_id: int,
) -> RoomState:
    room_id = _require_positive_int(room, "room_id")
    owner_id = _require_positive_int(room, "owner_id")
    max_player_count = _require_int(room, "max_player_count")
    robot_count = _require_int(room, "robot_count")
    if robot_count < 0:
        msg = "room.robot_count must not be negative."
        raise RoomStateDecodeError(msg)

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
            ai_count=robot_count,
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
    name = value.get("nickname")
    if not isinstance(name, str):
        msg = "room.persons nickname must be a string."
        raise RoomStateDecodeError(msg)
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
    result = value.get(field_name)
    if not isinstance(result, list):
        msg = f"room.{field_name} must be a list."
        raise RoomStateDecodeError(msg)
    return result


def _require_int(value: dict[str, JsonValue], field_name: str) -> int:
    result = value.get(field_name)
    if isinstance(result, bool) or not isinstance(result, int):
        msg = f"room.{field_name} must be an integer."
        raise RoomStateDecodeError(msg)
    return result


def _require_positive_int(
    value: dict[str, JsonValue],
    field_name: str,
) -> int:
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
