import pytest

from majsoulrpa.screens.match import AngangEvent, validate_seat, validate_tile


@pytest.mark.parametrize("wire_tile", ["0m", "5m"])
def test_angang_event_normalizes_red_five(wire_tile: str) -> None:
    event = AngangEvent.from_dict(
        3,
        {
            "seat": 1,
            "type": 3,
            "tiles": wire_tile,
            "doras": ["4p", "7z"],
        },
    )

    assert event == AngangEvent(
        action_step=3,
        seat=validate_seat(1),
        consumed=(
            validate_tile("0m"),
            validate_tile("5m"),
            validate_tile("5m"),
            validate_tile("5m"),
        ),
        dora_indicators=(validate_tile("4p"), validate_tile("7z")),
    )


def test_angang_event_expands_non_five_tile() -> None:
    event = AngangEvent.from_dict(
        3,
        {"seat": 1, "type": 3, "tiles": "7z", "doras": []},
    )

    assert event.consumed == ("7z",) * 4
    assert event.dora_indicators == ()


@pytest.mark.parametrize("type_", [2, 4])
def test_angang_event_rejects_other_action_types(type_: int) -> None:
    with pytest.raises(ValueError, match="identify angang"):
        AngangEvent.from_dict(
            3,
            {"seat": 1, "type": type_, "tiles": "7z", "doras": []},
        )
