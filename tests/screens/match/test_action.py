import base64

import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match import StartMatchEvent
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
