from dataclasses import FrozenInstanceError

import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match import (
    NewRoundEvent,
    validate_seat,
    validate_tile,
)


def _new_round_data(*, tiles: list[str]) -> dict[str, JsonValue]:
    return {
        "chang": 0,
        "ju": 1,
        "ben": 2,
        "liqibang": 1,
        "doras": ["3p"],
        "left_tile_count": 69,
        "scores": [25000, 24000, 26000, 25000],
        "tiles": tiles,
    }


def test_new_round_event_sorts_fourteen_tiles_before_separating_zimopai() -> (
    None
):
    data = _new_round_data(
        tiles=[
            "9s",
            "1m",
            "0m",
            "5m",
            "2p",
            "1z",
            "7z",
            "3m",
            "4m",
            "6m",
            "7m",
            "8m",
            "9m",
            "2m",
        ]
    )

    event = NewRoundEvent.from_dict(0, data)

    assert event == NewRoundEvent(
        action_step=0,
        chang=0,
        ju=validate_seat(1),
        ben=2,
        liqibang=1,
        dora_indicators=(validate_tile("3p"),),
        left_tile_count=69,
        scores=(25000, 24000, 26000, 25000),
        shoupai=tuple(
            validate_tile(tile)
            for tile in (
                "1m",
                "2m",
                "3m",
                "4m",
                "0m",
                "5m",
                "6m",
                "7m",
                "8m",
                "9m",
                "2p",
                "9s",
                "1z",
            )
        ),
        zimopai=validate_tile("7z"),
    )
    with pytest.raises(FrozenInstanceError):
        event.ben = 3  # ty: ignore[invalid-assignment]


def test_new_round_event_keeps_thirteen_tiles_in_shoupai() -> None:
    tiles = [
        "9s",
        "1m",
        "0m",
        "5m",
        "2p",
        "1z",
        "3m",
        "4m",
        "6m",
        "7m",
        "8m",
        "9m",
        "2m",
    ]

    event = NewRoundEvent.from_dict(1, _new_round_data(tiles=tiles))

    assert len(event.shoupai) == 13
    assert event.zimopai is None


@pytest.mark.parametrize(
    ("action_step", "updates"),
    [
        (2, {}),
        (0, {"chang": 3}),
        (0, {"ju": 4}),
        (0, {"ben": -1}),
        (0, {"liqibang": -1}),
        (0, {"doras": []}),
        (0, {"left_tile_count": 70}),
        (0, {"scores": [25000, 25000]}),
        (0, {"tiles": ["1m"] * 12}),
        (0, {"tiles": ["8z"] * 13}),
    ],
)
def test_new_round_event_rejects_invalid_values(
    action_step: int,
    updates: dict[str, JsonValue],
) -> None:
    data = _new_round_data(tiles=["1m"] * 13)
    data.update(updates)

    with pytest.raises(ValueError, match=r"must|Invalid"):
        NewRoundEvent.from_dict(action_step, data)
