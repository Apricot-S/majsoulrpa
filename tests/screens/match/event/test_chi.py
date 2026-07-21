import pytest

from majsoulrpa.screens.match import (
    ChiEvent,
    LiqiSuccess,
    validate_seat,
    validate_tile,
)


def test_chi_event_decodes_action_chi_peng_gang() -> None:
    event = ChiEvent.from_dict(
        3,
        {
            "seat": 1,
            "type": 0,
            "tiles": ["2m", "3m", "1m"],
            "froms": [1, 1, 0],
            "liqi": {
                "seat": 0,
                "score": 24000,
                "liqibang": 1,
                "failed": False,
            },
        },
    )

    assert event == ChiEvent(
        action_step=3,
        seat=validate_seat(1),
        from_seat=validate_seat(0),
        tile=validate_tile("1m"),
        consumed=(
            validate_tile("2m"),
            validate_tile("3m"),
        ),
        liqi_success=LiqiSuccess(
            seat=validate_seat(0),
            score=24000,
            liqibang=1,
            failed=False,
        ),
    )


def test_chi_event_rejects_tiles_that_do_not_form_a_sequence() -> None:
    with pytest.raises(ValueError, match="sequence"):
        ChiEvent.from_dict(
            3,
            {
                "seat": 1,
                "type": 0,
                "tiles": ["2m", "4m", "1m"],
                "froms": [1, 1, 0],
            },
        )
