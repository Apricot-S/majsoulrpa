from dataclasses import dataclass

from pydantic import JsonValue

from majsoulrpa.screens.match.state import (
    MatchOrigin,
    MatchPlayer,
    MatchRank,
)
from majsoulrpa.sniffer.events import DecodedRequestResponse, Direction

AUTH_GAME_NAME = ".lq.FastTest.authGame"
_CPU_LEVEL4 = MatchRank(id=10101, score=0)
_CPU_LEVEL3 = MatchRank(id=20101, score=0)


class MatchMetadataDecodeError(ValueError):
    pass


class MatchMetadataUnsupportedError(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class MatchMetadata:
    match_id: str
    origin: MatchOrigin
    origin_id: int
    self_seat: int
    players: tuple[MatchPlayer, ...]


def decode_match_metadata(
    message: DecodedRequestResponse,
    self_account_id: int,
) -> MatchMetadata:
    if message.raw.name != AUTH_GAME_NAME:
        msg = "Match metadata must come from authGame."
        raise MatchMetadataDecodeError(msg)
    if message.raw.request_direction is not Direction.OUTBOUND:
        msg = "authGame must be an outbound request/response."
        raise MatchMetadataDecodeError(msg)
    request_account_id = _get_int(message.request, "account_id")
    if request_account_id != self_account_id:
        msg = "authGame account ID must match the current account."
        raise MatchMetadataDecodeError(msg)
    match_id = _get_str(message.request, "game_uuid")
    if not match_id:
        msg = "authGame game UUID must not be empty."
        raise MatchMetadataDecodeError(msg)

    meta = _get_dict(_get_dict(message.response, "game_config"), "meta")
    room_id = _get_int(meta, "room_id")
    mode_id = _get_int(meta, "mode_id")
    contest_uid = _get_int(meta, "contest_uid")
    if room_id < 0 or mode_id < 0 or contest_uid < 0:
        msg = "authGame match origin IDs must be nonnegative."
        raise MatchMetadataDecodeError(msg)
    if room_id == 0 and contest_uid == 0:
        msg = "authGame identifies an unsupported match origin."
        raise MatchMetadataUnsupportedError(msg)
    if room_id > 0:
        if mode_id != 0 or contest_uid != 0:
            msg = "Friendly authGame metadata is inconsistent."
            raise MatchMetadataDecodeError(msg)
        origin = MatchOrigin.FRIENDLY
        origin_id = room_id
    else:
        origin = MatchOrigin.TOURNAMENT
        origin_id = contest_uid

    seat_list = _get_int_list(message.response, "seat_list")
    if len(seat_list) not in (3, 4):
        msg = "authGame seat list must contain three or four values."
        raise MatchMetadataDecodeError(msg)
    if seat_list.count(self_account_id) != 1:
        msg = "authGame seat list must contain the current account once."
        raise MatchMetadataDecodeError(msg)
    if any(value <= 0 for value in seat_list):
        msg = "authGame seat participant IDs must be positive."
        raise MatchMetadataDecodeError(msg)
    if len(seat_list) != len(set(seat_list)):
        msg = "authGame seat participant IDs must be unique."
        raise MatchMetadataDecodeError(msg)

    player_values = _get_dict_list(message.response, "players")
    robot_values = _get_dict_list(message.response, "robots")
    humans_by_id = _index_participants(player_values, kind="player")
    robots_by_id = _index_participants(robot_values, kind="robot")
    if set(humans_by_id) & set(robots_by_id):
        msg = "authGame human and robot IDs must not overlap."
        raise MatchMetadataDecodeError(msg)
    if set(seat_list) != set(humans_by_id) | set(robots_by_id):
        msg = "authGame seats must match all human and robot IDs."
        raise MatchMetadataDecodeError(msg)

    players: list[MatchPlayer] = []
    for seat, participant_id in enumerate(seat_list):
        human = humans_by_id.get(participant_id)
        if human is not None:
            players.append(
                _decode_human_player(human, participant_id, seat),
            )
            continue
        players.append(
            _decode_robot_player(
                seat,
                participant_id,
                robots_by_id[participant_id],
            ),
        )

    return MatchMetadata(
        match_id=match_id,
        origin=origin,
        origin_id=origin_id,
        self_seat=seat_list.index(self_account_id),
        players=tuple(players),
    )


def _decode_human_player(
    value: dict[str, JsonValue],
    account_id: int,
    seat: int,
) -> MatchPlayer:
    return MatchPlayer(
        seat=seat,
        account_id=account_id,
        name=_get_str(value, "nickname"),
        level4=_decode_rank(_get_dict(value, "level")),
        level3=_decode_rank(_get_dict(value, "level3")),
    )


def _decode_robot_player(
    seat: int,
    account_id: int,
    value: dict[str, JsonValue],
) -> MatchPlayer:
    name = _get_str(value, "nickname")
    if name:
        msg = "authGame robot nickname must be empty."
        raise MatchMetadataDecodeError(msg)
    return MatchPlayer(
        seat=seat,
        account_id=account_id,
        name=name,
        level4=_CPU_LEVEL4,
        level3=_CPU_LEVEL3,
    )


def _index_participants(
    values: list[dict[str, JsonValue]],
    *,
    kind: str,
) -> dict[int, dict[str, JsonValue]]:
    result: dict[int, dict[str, JsonValue]] = {}
    for value in values:
        participant_id = _get_int(value, "account_id")
        if participant_id <= 0:
            msg = f"authGame {kind} ID must be positive."
            raise MatchMetadataDecodeError(msg)
        if participant_id in result:
            msg = f"authGame {kind} IDs must be unique."
            raise MatchMetadataDecodeError(msg)
        result[participant_id] = value
    return result


def _decode_rank(value: dict[str, JsonValue]) -> MatchRank:
    rank_id = _get_int(value, "id")
    score = _get_int(value, "score")
    if rank_id <= 0:
        msg = "authGame rank ID must be positive."
        raise MatchMetadataDecodeError(msg)
    if score < 0:
        msg = "authGame rank score must be nonnegative."
        raise MatchMetadataDecodeError(msg)
    return MatchRank(id=rank_id, score=score)


def _get_dict(
    value: dict[str, JsonValue],
    name: str,
) -> dict[str, JsonValue]:
    result = value.get(name)
    if not isinstance(result, dict):
        msg = f"authGame {name} must be an object."
        raise MatchMetadataDecodeError(msg)
    return result


def _get_dict_list(
    value: dict[str, JsonValue],
    name: str,
) -> list[dict[str, JsonValue]]:
    result = value.get(name)
    if not isinstance(result, list) or not all(
        isinstance(item, dict) for item in result
    ):
        msg = f"authGame {name} must be a list of objects."
        raise MatchMetadataDecodeError(msg)
    return result


def _get_int(value: dict[str, JsonValue], name: str) -> int:
    result = value.get(name)
    if isinstance(result, bool) or not isinstance(result, int):
        msg = f"authGame {name} must be an int."
        raise MatchMetadataDecodeError(msg)
    return result


def _get_int_list(value: dict[str, JsonValue], name: str) -> list[int]:
    result = value.get(name)
    if not isinstance(result, list) or not all(
        isinstance(item, int) and not isinstance(item, bool) for item in result
    ):
        msg = f"authGame {name} must be a list of ints."
        raise MatchMetadataDecodeError(msg)
    return result


def _get_str(value: dict[str, JsonValue], name: str) -> str:
    result = value.get(name)
    if not isinstance(result, str):
        msg = f"authGame {name} must be a string."
        raise MatchMetadataDecodeError(msg)
    return result
