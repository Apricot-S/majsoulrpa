from dataclasses import dataclass

from pydantic import JsonValue

from majsoulrpa.screens.match.state import (
    MatchOrigin,
    MatchPlayer,
    MatchRank,
)
from majsoulrpa.sniffer.events import DecodedRequestResponse, Direction

AUTH_GAME_NAME = ".lq.FastTest.authGame"


class MatchMetadataDecodeError(ValueError):
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
    contest_uid = _get_int(meta, "contest_uid")
    if (room_id > 0) == (contest_uid > 0):
        msg = "authGame must identify one supported match origin."
        raise MatchMetadataDecodeError(msg)
    origin = MatchOrigin.FRIENDLY if room_id > 0 else MatchOrigin.TOURNAMENT
    origin_id = room_id if room_id > 0 else contest_uid

    seat_list = _get_int_list(message.response, "seat_list")
    if len(seat_list) not in (3, 4):
        msg = "authGame seat list must contain three or four values."
        raise MatchMetadataDecodeError(msg)
    if seat_list.count(self_account_id) != 1:
        msg = "authGame seat list must contain the current account once."
        raise MatchMetadataDecodeError(msg)
    positive_account_ids = [value for value in seat_list if value > 0]
    if len(positive_account_ids) != len(set(positive_account_ids)):
        msg = "authGame seat account IDs must be unique."
        raise MatchMetadataDecodeError(msg)

    player_values = _get_dict_list(message.response, "players")
    human_players = {
        account_id: _decode_human_player(value, account_id)
        for value in player_values
        if (account_id := _get_int(value, "account_id")) > 0
    }
    if set(human_players) != set(positive_account_ids):
        msg = "authGame players must match the positive seat account IDs."
        raise MatchMetadataDecodeError(msg)

    robot_values = iter(_get_dict_list(message.response, "robots"))
    players: list[MatchPlayer] = []
    for seat, account_id in enumerate(seat_list):
        if account_id > 0:
            player = human_players[account_id]
            players.append(
                MatchPlayer(
                    seat=seat,
                    account_id=player.account_id,
                    name=player.name,
                    level4=player.level4,
                    level3=player.level3,
                ),
            )
            continue
        robot = next(robot_values, None)
        players.append(_decode_robot_player(seat, robot))
    if next(robot_values, None) is not None:
        msg = "authGame contains more robots than CPU seats."
        raise MatchMetadataDecodeError(msg)

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
) -> MatchPlayer:
    return MatchPlayer(
        seat=0,
        account_id=account_id,
        name=_get_str(value, "nickname"),
        level4=_decode_rank(_get_dict(value, "level")),
        level3=_decode_rank(_get_dict(value, "level3")),
    )


def _decode_robot_player(
    seat: int,
    value: dict[str, JsonValue] | None,
) -> MatchPlayer:
    if value is None:
        return MatchPlayer(
            seat=seat,
            account_id=None,
            name=None,
            level4=None,
            level3=None,
        )
    name = value.get("nickname")
    if not isinstance(name, str) or not name:
        name = None
    return MatchPlayer(
        seat=seat,
        account_id=None,
        name=name,
        level4=_decode_optional_rank(value.get("level")),
        level3=_decode_optional_rank(value.get("level3")),
    )


def _decode_rank(value: dict[str, JsonValue]) -> MatchRank:
    return MatchRank(id=_get_int(value, "id"), score=_get_int(value, "score"))


def _decode_optional_rank(value: JsonValue | None) -> MatchRank | None:
    if not isinstance(value, dict):
        return None
    rank_id = value.get("id")
    score = value.get("score")
    if (
        isinstance(rank_id, bool)
        or not isinstance(rank_id, int)
        or rank_id <= 0
        or isinstance(score, bool)
        or not isinstance(score, int)
        or score < 0
    ):
        return None
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
