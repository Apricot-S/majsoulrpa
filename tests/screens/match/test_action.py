import base64

import pytest
from pydantic import JsonValue

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.match import NewRoundEvent, StartMatchEvent, ZimoEvent
from majsoulrpa.screens.match._action import (
    MatchActionDecodeError,
    decode_live_action,
    decode_restore_action,
)
from tests.screens.match._support import _live_action


def test_live_action_mj_start_decodes_to_start_match_event() -> None:
    event, _ = decode_live_action(_live_action())

    assert event == StartMatchEvent(action_step=0)


def test_live_action_replaces_obfuscated_data_with_decoded_message() -> None:
    message = _live_action()

    event, decoded_message = decode_live_action(message)

    assert event == StartMatchEvent(action_step=0)
    assert decoded_message.raw is message.raw
    assert decoded_message.message == {
        "step": 0,
        "name": "ActionMJStart",
        "data": {},
    }


def test_restore_action_mj_start_decodes_to_start_match_event() -> None:
    event, decoded_action = decode_restore_action(
        {"step": 0, "name": "ActionMJStart", "data": ""}
    )

    assert event == StartMatchEvent(action_step=0)
    assert decoded_action == {
        "step": 0,
        "name": "ActionMJStart",
        "data": {},
    }


def test_restore_action_ignores_unknown_protobuf_fields() -> None:
    event, decoded_action = decode_restore_action(
        {
            "step": 0,
            "name": "ActionMJStart",
            "data": base64.b64encode(b"\x08\x01").decode(),
        }
    )

    assert event == StartMatchEvent(action_step=0)
    assert decoded_action["data"] == {}


def test_live_and_restore_action_new_round_decode_to_same_event() -> None:
    data = liqi_pb2.ActionNewRound(
        chang=0,
        ju=1,
        ben=0,
        tiles=["1m"] * 13,
        scores=[25000] * 4,
        liqibang=0,
        left_tile_count=69,
        doras=["3p"],
    ).SerializeToString()
    live_event, _ = decode_live_action(
        _live_action(step=0, name="ActionNewRound", data=data)
    )
    restore_event, _ = decode_restore_action(
        {
            "step": 0,
            "name": "ActionNewRound",
            "data": base64.b64encode(data).decode(),
        }
    )

    expected = NewRoundEvent.from_dict(
        0,
        {
            "chang": 0,
            "ju": 1,
            "ben": 0,
            "tiles": ["1m"] * 13,
            "dora": "",
            "scores": [25000] * 4,
            "liqibang": 0,
            "tingpais0": [],
            "tingpais1": [],
            "al": False,
            "md5": "",
            "left_tile_count": 69,
            "doras": ["3p"],
            "opens": [],
            "ju_count": 0,
            "field_spell": 0,
            "sha256": "",
            "saltSha256": "",
        },
    )
    assert live_event == expected
    assert restore_event == expected


def test_live_and_restore_action_deal_tile_decode_to_same_event() -> None:
    data = liqi_pb2.ActionDealTile(
        seat=0,
        tile="5m",
        left_tile_count=68,
        doras=["3p"],
    ).SerializeToString()
    live_event, _ = decode_live_action(
        _live_action(step=2, name="ActionDealTile", data=data)
    )
    restore_event, _ = decode_restore_action(
        {
            "step": 2,
            "name": "ActionDealTile",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert isinstance(live_event, ZimoEvent)
    assert live_event == restore_event


@pytest.mark.parametrize(
    "action",
    [
        {"step": True, "name": "ActionMJStart", "data": ""},
        {"step": -1, "name": "ActionMJStart", "data": ""},
        {"step": 0, "name": "ActionUnknown", "data": ""},
        {"step": 0, "name": "ActionMJStart", "data": "%%%"},
        {
            "step": 0,
            "name": "ActionMJStart",
            "data": base64.b64encode(b"not-empty").decode(),
        },
    ],
)
def test_restore_action_rejects_invalid_action(
    action: dict[str, JsonValue],
) -> None:
    with pytest.raises(MatchActionDecodeError):
        decode_restore_action(action)
