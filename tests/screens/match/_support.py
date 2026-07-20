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


def _live_new_round_action(*, step: int) -> DecodedNotice:
    data = liqi_pb2.ActionNewRound(
        chang=0,
        ju=0,
        ben=0,
        tiles=["1m"] * 13,
        scores=[25000] * 4,
        liqibang=0,
        left_tile_count=69,
        doras=["3p"],
    ).SerializeToString()
    return _live_action(step=step, name="ActionNewRound", data=data)


def _auth_game() -> DecodedRequestResponse:
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
                    (SELF_ACCOUNT_ID, 100002, 100003, 100004),
                )
            ],
            "seat_list": [SELF_ACCOUNT_ID, 100002, 100003, 100004],
            "game_config": {
                "meta": {"room_id": 12345, "contest_uid": 0},
            },
            "robots": [],
        },
    )
