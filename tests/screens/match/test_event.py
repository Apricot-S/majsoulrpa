import datetime
from dataclasses import FrozenInstanceError

import pytest

from majsoulrpa.screens.match import StartMatchEvent


def test_start_match_event_is_an_immutable_validated_value() -> None:
    observed_at = datetime.datetime(2026, 1, 2, tzinfo=datetime.UTC)
    event = StartMatchEvent(action_step=0, observed_at=observed_at)

    assert event.action_step == 0
    assert event.observed_at == observed_at
    with pytest.raises(FrozenInstanceError):
        event.action_step = 1  # ty: ignore[invalid-assignment]


def test_start_match_event_rejects_negative_action_step() -> None:
    with pytest.raises(ValueError, match="nonnegative"):
        StartMatchEvent(
            action_step=-1,
            observed_at=None,
        )


def test_start_match_event_rejects_naive_observed_at() -> None:
    with pytest.raises(ValueError, match="timezone-aware"):
        StartMatchEvent(
            action_step=0,
            observed_at=datetime.datetime(2026, 1, 2),  # noqa: DTZ001
        )
