from dataclasses import FrozenInstanceError

import pytest

from majsoulrpa.screens.match import StartMatchEvent


def test_start_match_event_is_an_immutable_validated_value() -> None:
    event = StartMatchEvent(action_step=0)

    assert event.action_step == 0
    with pytest.raises(FrozenInstanceError):
        event.action_step = 1  # ty: ignore[invalid-assignment]


def test_start_match_event_rejects_negative_action_step() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        StartMatchEvent(action_step=-1)


def test_start_match_event_from_decoded_dict() -> None:
    event = StartMatchEvent.from_dict(0, {})

    assert event == StartMatchEvent(action_step=0)
