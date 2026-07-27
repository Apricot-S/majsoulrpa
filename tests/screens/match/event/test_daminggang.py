import pytest

from majsoulrpa.screens.match import (
    DaminggangEvent,
    LiqiSuccess,
    validate_seat,
    validate_tile,
)


def test_daminggang_event_decodes_action_chi_peng_gang() -> None:
    event = DaminggangEvent.from_dict(
        3,
        {
            "seat": 1,
            "type": 2,
            "tiles": ["0m", "5m", "5m", "5m"],
            "froms": [1, 1, 1, 3],
            "liqi": {
                "seat": 3,
                "score": 24000,
                "liqibang": 1,
                "failed": False,
            },
        },
    )

    assert event == DaminggangEvent(
        action_step=3,
        seat=validate_seat(1),
        from_seat=validate_seat(3),
        tile=validate_tile("5m"),
        consumed=(
            validate_tile("0m"),
            validate_tile("5m"),
            validate_tile("5m"),
        ),
        liqi_success=LiqiSuccess(
            seat=validate_seat(3),
            score=24000,
            liqibang=1,
            failed=False,
        ),
    )


def test_daminggang_event_rejects_tiles_of_different_kinds() -> None:
    with pytest.raises(ValueError, match="same kind"):
        DaminggangEvent.from_dict(
            3,
            {
                "seat": 1,
                "type": 2,
                "tiles": ["5m", "5m", "5p", "5m"],
                "froms": [1, 1, 1, 3],
            },
        )


def test_daminggang_event_rejects_invalid_tile_sources() -> None:
    with pytest.raises(ValueError, match="first three"):
        DaminggangEvent.from_dict(
            3,
            {
                "seat": 1,
                "type": 2,
                "tiles": ["5m", "5m", "5m", "5m"],
                "froms": [1, 1, 3, 3],
            },
        )
