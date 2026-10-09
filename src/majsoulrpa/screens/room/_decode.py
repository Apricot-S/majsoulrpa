from pydantic import JsonValue

from majsoulrpa.screens._json_fields import get_int, get_list, get_str
from majsoulrpa.screens.errors import MessageDecodeError
from majsoulrpa.screens.room.state import RoomPlayer, RoomState, RoomStatus


def decode_room_state(
    room: dict[str, JsonValue],
    *,
    version: int,
    self_account_id: int,
) -> RoomState:
    room_id = _require_positive_int(room, "room_id")
    owner_id = _require_positive_int(room, "owner_id")
    max_player_count = get_int(room, "max_player_count")
    robots = get_list(room, "robots")

    ready_list = get_list(room, "ready_list")
    ready_account_ids = {
        _require_positive_list_int(value, "room.ready_list")
        for value in ready_list
    }

    persons = get_list(room, "persons")
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
        raise MessageDecodeError(msg)

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
        raise MessageDecodeError(str(error)) from error


def _decode_room_player(
    value: JsonValue,
    *,
    owner_id: int,
    ready_account_ids: set[int],
) -> RoomPlayer:
    if not isinstance(value, dict):
        msg = "room.persons entries must be objects."
        raise MessageDecodeError(msg)
    account_id = _require_positive_int(value, "account_id")
    name = get_str(value, "nickname")
    return RoomPlayer(
        account_id=account_id,
        name=name,
        is_host=account_id == owner_id,
        is_ready=account_id in ready_account_ids,
    )


def _require_positive_int(value: dict[str, JsonValue], field_name: str) -> int:
    result = get_int(value, field_name)
    if result <= 0:
        msg = f"room.{field_name} must be positive."
        raise MessageDecodeError(msg)
    return result


def _require_positive_list_int(value: JsonValue, field_name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value <= 0:
        msg = f"{field_name} entries must be positive integers."
        raise MessageDecodeError(msg)
    return value
