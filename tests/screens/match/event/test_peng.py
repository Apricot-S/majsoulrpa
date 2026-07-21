import pytest

from majsoulrpa.screens.match import (
    LiqiSuccess,
    PengEvent,
    validate_seat,
    validate_tile,
)


def test_peng_event_decodes_action_chi_peng_gang() -> None:
    event = PengEvent.from_dict(
        3,
        {
            "seat": 1,
            "type": 1,
            "tiles": ["0m", "5m", "5m"],
            "froms": [1, 1, 3],
            "liqi": {
                "seat": 3,
                "score": 24000,
                "liqibang": 1,
                "failed": False,
            },
        },
    )

    assert event == PengEvent(
        action_step=3,
        seat=validate_seat(1),
        from_seat=validate_seat(3),
        tile=validate_tile("5m"),
        consumed=(validate_tile("0m"), validate_tile("5m")),
        liqi_success=LiqiSuccess(
            seat=validate_seat(3),
            score=24000,
            liqibang=1,
            failed=False,
        ),
    )


def test_peng_event_rejects_tiles_of_different_kinds() -> None:
    with pytest.raises(ValueError, match="same kind"):
        PengEvent.from_dict(
            3,
            {
                "seat": 1,
                "type": 1,
                "tiles": ["5m", "5p", "5m"],
                "froms": [1, 1, 3],
            },
        )
