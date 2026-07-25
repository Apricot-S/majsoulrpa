from types import SimpleNamespace
from typing import cast

import pytest

from majsoulrpa.screens.match import (
    ChiOperation,
    DaminggangOperation,
    Hule,
    HuleEvent,
    MatchOperation,
    MatchScreen,
    MatchState,
    PengOperation,
)
from majsoulrpa.screens.match.types import validate_seat, validate_tile


def _hule(seat: int) -> Hule:
    return Hule(
        hand=(),
        ming=(),
        hu_tile=validate_tile("5m"),
        seat=validate_seat(seat),
        zimo=False,
        qinjia=False,
        liqi=False,
        dora_indicators=(),
        li_dora_indicators=(),
        yiman=False,
        count=0,
        fans=(),
        fu=0,
        point_rong=0,
        point_zimo_qin=0,
        point_zimo_xian=0,
        title_id=0,
        point_sum=0,
        dadian=0,
        baopai_seat=None,
        baopai_seats=(),
    )


def _hule_event(*seats: int) -> HuleEvent:
    return HuleEvent(
        action_step=2,
        hules=tuple(_hule(seat) for seat in seats),
        old_scores=(25000,) * 4,
        delta_scores=(0,) * 4,
        scores=(25000,) * 4,
        baopai_seat=None,
    )


@pytest.fixture
def state() -> MatchState:
    return cast(
        "MatchState",
        SimpleNamespace(self_seat=validate_seat(0)),
    )


@pytest.mark.parametrize(
    "operation",
    [
        ChiOperation(
            from_seat=validate_seat(3),
            tile=validate_tile("5m"),
            consumed=(validate_tile("3m"), validate_tile("4m")),
        ),
        PengOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
        ),
        DaminggangOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(
                validate_tile("0m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
        ),
    ],
)
def test_opponents_hule_preempts_fulu_operation(
    state: MatchState,
    operation: MatchOperation,
) -> None:
    event = _hule_event(1, 2)

    assert MatchScreen._event_preempts_operation(state, event, operation)


@pytest.mark.parametrize(
    "operation",
    [
        ChiOperation(
            from_seat=validate_seat(3),
            tile=validate_tile("5m"),
            consumed=(validate_tile("3m"), validate_tile("4m")),
        ),
        PengOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(validate_tile("0m"), validate_tile("5m")),
        ),
        DaminggangOperation(
            from_seat=validate_seat(2),
            tile=validate_tile("5m"),
            consumed=(
                validate_tile("0m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
        ),
    ],
)
def test_hule_containing_self_does_not_preempt_fulu_operation(
    state: MatchState,
    operation: MatchOperation,
) -> None:
    event = _hule_event(0, 1)

    assert not MatchScreen._event_preempts_operation(state, event, operation)
