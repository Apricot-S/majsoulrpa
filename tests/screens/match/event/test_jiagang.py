import pytest

from majsoulrpa.screens.match import (
    JiagangEvent,
    validate_seat,
    validate_tile,
)


@pytest.mark.parametrize("added", ["0m", "5m"])
def test_jiagang_event_preserves_added_tile(added: str) -> None:
    event = JiagangEvent.from_dict(
        3,
        {
            "seat": 1,
            "type": 2,
            "tiles": added,
            "doras": ["4p", "7z"],
        },
    )

    assert event == JiagangEvent(
        action_step=3,
        seat=validate_seat(1),
        added=validate_tile(added),
        dora_indicators=(validate_tile("4p"), validate_tile("7z")),
    )


@pytest.mark.parametrize("type_", [3, 4])
def test_jiagang_event_rejects_other_action_types(type_: int) -> None:
    with pytest.raises(ValueError, match="identify jiagang"):
        JiagangEvent.from_dict(
            3,
            {"seat": 1, "type": type_, "tiles": "7z", "doras": []},
        )
