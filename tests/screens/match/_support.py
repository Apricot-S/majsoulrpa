import base64
import datetime

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.sniffer.events import (
    DecodedNotice,
    DecodedRequestResponse,
    Direction,
    RawNotice,
    RawRequestResponse,
)

OBSERVED_AT = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
SELF_ACCOUNT_ID = 100001


def _obfuscate_action_data(data: bytes) -> bytes:
    keys = (132, 94, 78, 66, 57, 162, 31, 96, 28)
    result = bytearray(data)
    for index, value in enumerate(result):
        mask = (
            (23 ^ len(result)) + 5 * index + keys[index % len(keys)]
        ) & 0xFF
        result[index] = value ^ mask
    return bytes(result)


def _live_action(
    *,
    step: int = 0,
    name: str = "ActionMJStart",
    data: bytes = b"",
) -> DecodedNotice:
    encoded_data = base64.b64encode(_obfuscate_action_data(data)).decode()
    return DecodedNotice(
        raw=RawNotice(
            direction=Direction.INBOUND,
            name=".lq.ActionPrototype",
            payload=b"synthetic-action",
            observed_at=OBSERVED_AT,
        ),
        message={"step": step, "name": name, "data": encoded_data},
    )


def _live_new_round_action(
    *,
    step: int,
    tiles: list[str] | None = None,
    scores: list[int] | None = None,
    ju: int = 0,
    operation: liqi_pb2.OptionalOperationList | None = None,
) -> DecodedNotice:
    data = liqi_pb2.ActionNewRound(
        chang=0,
        ju=ju,
        ben=0,
        tiles=["1m"] * 13 if tiles is None else tiles,
        scores=[25000] * 4 if scores is None else scores,
        liqibang=0,
        left_tile_count=69,
        doras=["3p"],
        operation=operation,
    ).SerializeToString()
    return _live_action(step=step, name="ActionNewRound", data=data)


def _live_discard_action(
    *,
    step: int,
    seat: int,
    tile: str,
    moqie: bool,
    liqi: bool = False,
    wliqi: bool = False,
    doras: list[str] | None = None,
    operation: liqi_pb2.OptionalOperationList | None = None,
) -> DecodedNotice:
    data = liqi_pb2.ActionDiscardTile(
        seat=seat,
        tile=tile,
        moqie=moqie,
        is_liqi=liqi,
        is_wliqi=wliqi,
        doras=[] if doras is None else doras,
        operation=operation,
    ).SerializeToString()
    return _live_action(step=step, name="ActionDiscardTile", data=data)


def _live_deal_action(
    *,
    step: int,
    seat: int,
    tile: str,
    left_tile_count: int,
    doras: list[str] | None = None,
    liqi: liqi_pb2.LiQiSuccess | None = None,
    operation: liqi_pb2.OptionalOperationList | None = None,
) -> DecodedNotice:
    data = liqi_pb2.ActionDealTile(
        seat=seat,
        tile=tile,
        left_tile_count=left_tile_count,
        doras=[] if doras is None else doras,
        liqi=liqi,
        operation=operation,
    ).SerializeToString()
    return _live_action(step=step, name="ActionDealTile", data=data)


def _live_chi_action(
    *,
    step: int,
    seat: int,
    tiles: list[str],
    froms: list[int],
    liqi: liqi_pb2.LiQiSuccess | None = None,
    operation: liqi_pb2.OptionalOperationList | None = None,
) -> DecodedNotice:
    return _live_chi_peng_gang_action(
        step=step,
        seat=seat,
        type_=0,
        tiles=tiles,
        froms=froms,
        liqi=liqi,
        operation=operation,
    )


def _live_peng_action(
    *,
    step: int,
    seat: int,
    tiles: list[str],
    froms: list[int],
    liqi: liqi_pb2.LiQiSuccess | None = None,
    operation: liqi_pb2.OptionalOperationList | None = None,
) -> DecodedNotice:
    return _live_chi_peng_gang_action(
        step=step,
        seat=seat,
        type_=1,
        tiles=tiles,
        froms=froms,
        liqi=liqi,
        operation=operation,
    )


def _live_chi_peng_gang_action(
    *,
    step: int,
    seat: int,
    type_: int,
    tiles: list[str],
    froms: list[int],
    liqi: liqi_pb2.LiQiSuccess | None,
    operation: liqi_pb2.OptionalOperationList | None,
) -> DecodedNotice:
    data = liqi_pb2.ActionChiPengGang(
        seat=seat,
        type=type_,
        tiles=tiles,
        froms=froms,
        liqi=liqi,
        operation=operation,
    ).SerializeToString()
    return _live_action(step=step, name="ActionChiPengGang", data=data)


def _auth_game(
    *,
    player_count: int = 4,
    cpu_count: int = 0,
    room_id: int = 12345,
    mode_id: int = 0,
    contest_uid: int = 0,
    seat_list: tuple[int, ...] | None = None,
) -> DecodedRequestResponse:
    human_account_ids = (
        SELF_ACCOUNT_ID,
        100002,
        100003,
        100004,
    )[: player_count - cpu_count]
    robot_ids = tuple(range(1, cpu_count + 1))
    if seat_list is None:
        seat_list = (*human_account_ids, *robot_ids)
    return DecodedRequestResponse(
        raw=RawRequestResponse(
            request_direction=Direction.OUTBOUND,
            name=".lq.FastTest.authGame",
            request=b"synthetic-request",
            response=b"synthetic-response",
            request_observed_at=OBSERVED_AT,
            response_observed_at=OBSERVED_AT,
        ),
        request={
            "account_id": SELF_ACCOUNT_ID,
            "token": "synthetic-secret-token",
            "game_uuid": "synthetic-match-id",
        },
        response={
            "players": [
                {
                    "account_id": account_id,
                    "nickname": f"player-{seat}",
                    "level": {"id": 10101 + seat, "score": seat},
                    "level3": {"id": 20101 + seat, "score": seat + 10},
                }
                for seat, account_id in enumerate(
                    human_account_ids,
                )
            ],
            "seat_list": list(seat_list),
            "game_config": {
                "meta": {
                    "room_id": room_id,
                    "mode_id": mode_id,
                    "contest_uid": contest_uid,
                },
            },
            "robots": [
                {"account_id": robot_id, "nickname": ""}
                for robot_id in robot_ids
            ],
        },
    )
