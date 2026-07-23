import base64

import pytest
from pydantic import JsonValue

from majsoulrpa.assets.protocol import liqi_pb2
from majsoulrpa.screens.match import (
    AngangEvent,
    ChiEvent,
    DaminggangEvent,
    JiagangEvent,
    NewRoundEvent,
    PengEvent,
    StartMatchEvent,
    ZimoEvent,
)
from majsoulrpa.screens.match._action import (
    MatchActionDecodeError,
    decode_live_action,
    decode_restore_action,
)
from majsoulrpa.screens.match.operation._specification import (
    _AngangOperationSpecification,
    _ChiOperationSpecification,
    _DaminggangOperationSpecification,
)
from tests.screens.match._support import _live_action


def test_live_action_mj_start_decodes_to_start_match_event() -> None:
    event, operation, _ = decode_live_action(_live_action())

    assert event == StartMatchEvent(action_step=0)
    assert operation is None


def test_live_action_replaces_obfuscated_data_with_decoded_message() -> None:
    message = _live_action()

    event, _, decoded_message = decode_live_action(message)

    assert event == StartMatchEvent(action_step=0)
    assert decoded_message.raw is message.raw
    assert decoded_message.message == {
        "step": 0,
        "name": "ActionMJStart",
        "data": {},
    }


def test_restore_action_mj_start_decodes_to_start_match_event() -> None:
    event, _, decoded_action = decode_restore_action(
        {"step": 0, "name": "ActionMJStart", "data": ""}
    )

    assert event == StartMatchEvent(action_step=0)
    assert decoded_action == {
        "step": 0,
        "name": "ActionMJStart",
        "data": {},
    }


def test_restore_action_ignores_unknown_protobuf_fields() -> None:
    event, _, decoded_action = decode_restore_action(
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
    live_event, _, _ = decode_live_action(
        _live_action(step=0, name="ActionNewRound", data=data)
    )
    restore_event, _, _ = decode_restore_action(
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
        operation=liqi_pb2.OptionalOperationList(
            time_fixed=5000,
            time_add=20000,
            operation_list=[liqi_pb2.OptionalOperation(type=1)],
        ),
    ).SerializeToString()
    live_event, live_operation, _ = decode_live_action(
        _live_action(step=2, name="ActionDealTile", data=data)
    )
    restore_event, restore_operation, _ = decode_restore_action(
        {
            "step": 2,
            "name": "ActionDealTile",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert isinstance(live_event, ZimoEvent)
    assert live_event == restore_event
    assert live_operation is not None
    assert live_operation == restore_operation


def test_live_and_restore_discard_decode_same_chi_specification() -> None:
    data = liqi_pb2.ActionDiscardTile(
        seat=3,
        tile="5m",
        operation=liqi_pb2.OptionalOperationList(
            time_fixed=5000,
            time_add=20000,
            operation_list=[
                liqi_pb2.OptionalOperation(
                    type=2,
                    combination=["3m|4m", "4m|6m"],
                )
            ],
        ),
    ).SerializeToString()
    _, live_operation, _ = decode_live_action(
        _live_action(step=2, name="ActionDiscardTile", data=data)
    )
    _, restore_operation, _ = decode_restore_action(
        {
            "step": 2,
            "name": "ActionDiscardTile",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert live_operation is not None
    assert live_operation == restore_operation
    [operation] = live_operation.operations
    assert isinstance(operation, _ChiOperationSpecification)
    assert operation.consumed_candidates == (
        ("3m", "4m"),
        ("4m", "6m"),
    )


def test_live_restore_daminggang_specification() -> None:
    data = liqi_pb2.ActionDiscardTile(
        seat=2,
        tile="5m",
        operation=liqi_pb2.OptionalOperationList(
            time_fixed=5000,
            time_add=20000,
            operation_list=[
                liqi_pb2.OptionalOperation(
                    type=5,
                    combination=["0m|5m|5m"],
                )
            ],
        ),
    ).SerializeToString()
    _, live_operation, _ = decode_live_action(
        _live_action(step=2, name="ActionDiscardTile", data=data)
    )
    _, restore_operation, _ = decode_restore_action(
        {
            "step": 2,
            "name": "ActionDiscardTile",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert live_operation is not None
    assert live_operation == restore_operation
    [operation] = live_operation.operations
    assert isinstance(operation, _DaminggangOperationSpecification)
    assert operation.consumed_candidates == (("0m", "5m", "5m"),)


def test_live_restore_angang_specification() -> None:
    data = liqi_pb2.ActionDealTile(
        seat=0,
        tile="5m",
        operation=liqi_pb2.OptionalOperationList(
            time_fixed=5000,
            time_add=20000,
            operation_list=[
                liqi_pb2.OptionalOperation(
                    type=4,
                    combination=["0m|5m|5m|5m"],
                )
            ],
        ),
    ).SerializeToString()
    _, live_operation, _ = decode_live_action(
        _live_action(step=2, name="ActionDealTile", data=data)
    )
    _, restore_operation, _ = decode_restore_action(
        {
            "step": 2,
            "name": "ActionDealTile",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert live_operation is not None
    assert live_operation == restore_operation
    [operation] = live_operation.operations
    assert isinstance(operation, _AngangOperationSpecification)
    assert operation.consumed_candidates == (("0m", "5m", "5m", "5m"),)


def test_live_and_restore_action_chi_decode_to_same_event() -> None:
    data = liqi_pb2.ActionChiPengGang(
        seat=1,
        type=0,
        tiles=["2m", "3m", "1m"],
        froms=[1, 1, 0],
    ).SerializeToString()
    live_event, live_operation, _ = decode_live_action(
        _live_action(step=3, name="ActionChiPengGang", data=data)
    )
    restore_event, restore_operation, _ = decode_restore_action(
        {
            "step": 3,
            "name": "ActionChiPengGang",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert isinstance(live_event, ChiEvent)
    assert live_event == restore_event
    assert live_operation is None
    assert restore_operation is None


def test_live_and_restore_action_peng_decode_to_same_event() -> None:
    data = liqi_pb2.ActionChiPengGang(
        seat=1,
        type=1,
        tiles=["0m", "5m", "5m"],
        froms=[1, 1, 3],
    ).SerializeToString()
    live_event, live_operation, _ = decode_live_action(
        _live_action(step=3, name="ActionChiPengGang", data=data)
    )
    restore_event, restore_operation, _ = decode_restore_action(
        {
            "step": 3,
            "name": "ActionChiPengGang",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert isinstance(live_event, PengEvent)
    assert live_event == restore_event
    assert live_operation is None
    assert restore_operation is None


def test_live_and_restore_action_daminggang_decode_to_same_event() -> None:
    data = liqi_pb2.ActionChiPengGang(
        seat=1,
        type=2,
        tiles=["0m", "5m", "5m", "5m"],
        froms=[1, 1, 1, 3],
    ).SerializeToString()
    live_event, live_operation, _ = decode_live_action(
        _live_action(step=3, name="ActionChiPengGang", data=data)
    )
    restore_event, restore_operation, _ = decode_restore_action(
        {
            "step": 3,
            "name": "ActionChiPengGang",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert isinstance(live_event, DaminggangEvent)
    assert live_event == restore_event
    assert live_operation is None
    assert restore_operation is None


def test_action_chi_peng_gang_rejects_unimplemented_type() -> None:
    data = liqi_pb2.ActionChiPengGang(
        seat=1,
        type=3,
        tiles=["1m", "1m", "1m"],
        froms=[1, 1, 0],
    ).SerializeToString()

    with pytest.raises(MatchActionDecodeError):
        decode_restore_action(
            {
                "step": 3,
                "name": "ActionChiPengGang",
                "data": base64.b64encode(data).decode(),
            }
        )


def test_live_and_restore_action_angang_decode_to_same_event() -> None:
    data = liqi_pb2.ActionAnGangAddGang(
        seat=1,
        type=3,
        tiles="5m",
        doras=["4p"],
    ).SerializeToString()
    live_event, live_operation, _ = decode_live_action(
        _live_action(step=3, name="ActionAnGangAddGang", data=data)
    )
    restore_event, restore_operation, _ = decode_restore_action(
        {
            "step": 3,
            "name": "ActionAnGangAddGang",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert isinstance(live_event, AngangEvent)
    assert live_event == restore_event
    assert live_operation is None
    assert restore_operation is None


def test_live_and_restore_action_jiagang_decode_to_same_event() -> None:
    data = liqi_pb2.ActionAnGangAddGang(
        seat=1,
        type=2,
        tiles="0m",
        doras=["4p"],
    ).SerializeToString()
    live_event, live_operation, _ = decode_live_action(
        _live_action(step=3, name="ActionAnGangAddGang", data=data)
    )
    restore_event, restore_operation, _ = decode_restore_action(
        {
            "step": 3,
            "name": "ActionAnGangAddGang",
            "data": base64.b64encode(data).decode(),
        }
    )

    assert isinstance(live_event, JiagangEvent)
    assert live_event == restore_event
    assert live_event.added == "0m"
    assert live_operation is None
    assert restore_operation is None


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
