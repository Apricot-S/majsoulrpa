import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match import (
    LiqiSuccess,
    ZimoEvent,
    validate_seat,
    validate_tile,
)


def test_zimo_event_from_dict() -> None:
    event = ZimoEvent.from_dict(
        3,
        {
            "seat": 0,
            "tile": "0m",
            "left_tile_count": 68,
            "doras": ["3p", "7z"],
            "liqi": {
                "seat": 3,
                "score": 24000,
                "liqibang": 1,
                "failed": False,
            },
        },
    )

    assert event == ZimoEvent(
        action_step=3,
        seat=validate_seat(0),
        tile=validate_tile("0m"),
        left_tile_count=68,
        dora_indicators=(validate_tile("3p"), validate_tile("7z")),
        liqi_success=LiqiSuccess(
            seat=validate_seat(3),
            score=24000,
            liqibang=1,
            failed=False,
        ),
    )


def test_zimo_event_normalizes_concealed_tile_to_none() -> None:
    event = ZimoEvent.from_dict(
        2,
        {
            "seat": 1,
            "tile": "",
            "left_tile_count": 67,
            "doras": [],
        },
    )

    assert event.tile is None
    assert event.liqi_success is None


@pytest.mark.parametrize(
    "data",
    [
        {
            "seat": 4,
            "tile": "",
            "left_tile_count": 68,
            "doras": [],
        },
        {
            "seat": 0,
            "tile": "1x",
            "left_tile_count": 68,
            "doras": [],
        },
        {
            "seat": 0,
            "tile": "1m",
            "left_tile_count": 70,
            "doras": [],
        },
        {
            "seat": 0,
            "tile": "1m",
            "left_tile_count": 68,
            "doras": [],
            "liqi": [],
        },
    ],
)
def test_zimo_event_rejects_invalid_fields(
    data: dict[str, JsonValue],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        ZimoEvent.from_dict(2, data)
