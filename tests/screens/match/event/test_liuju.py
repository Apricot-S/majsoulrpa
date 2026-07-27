import pytest

from majsoulrpa.screens.match import (
    LiqiSuccess,
    LiujuEvent,
    LiujuType,
    Seat,
    validate_seat,
)


@pytest.mark.parametrize(
    ("wire_type", "wire_seat", "expected_type", "expected_seat"),
    [
        (1, 2, LiujuType.JIUZHONGJIUPAI, validate_seat(2)),
        (2, 0, LiujuType.SIFENGLIANDA, None),
        (3, 0, LiujuType.SIGANGSANLE, None),
        (4, 0, LiujuType.SIJIALIQI, None),
    ],
)
def test_liuju_event_decodes_type_and_seat(
    wire_type: int,
    wire_seat: int,
    expected_type: LiujuType,
    expected_seat: Seat | None,
) -> None:
    event = LiujuEvent.from_dict(
        4,
        {
            "type": wire_type,
            "seat": wire_seat,
        },
    )

    assert event == LiujuEvent(
        action_step=4,
        type=expected_type,
        seat=expected_seat,
    )


@pytest.mark.parametrize("wire_type", [0, 5])
def test_liuju_event_rejects_unknown_type(wire_type: int) -> None:
    with pytest.raises(ValueError, match="not supported"):
        LiujuEvent.from_dict(
            4,
            {
                "type": wire_type,
                "seat": 0,
            },
        )


@pytest.mark.parametrize("wire_type", [2, 3, 4])
def test_liuju_event_rejects_seat_for_non_jiuzhongjiupai(
    wire_type: int,
) -> None:
    with pytest.raises(ValueError, match="seat must be zero"):
        LiujuEvent.from_dict(
            4,
            {
                "type": wire_type,
                "seat": 1,
            },
        )


def test_liuju_event_preserves_liqi_success() -> None:
    event = LiujuEvent.from_dict(
        4,
        {
            "type": 4,
            "seat": 0,
            "liqi": {
                "seat": 2,
                "score": 24000,
                "liqibang": 1,
                "failed": False,
            },
        },
    )

    assert event.liqi_success == LiqiSuccess(
        seat=validate_seat(2),
        score=24000,
        liqibang=1,
        failed=False,
    )
