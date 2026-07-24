import pytest

from majsoulrpa.screens.match import BabeiEvent, validate_seat, validate_tile


def test_babei_event_preserves_moqie_and_doras() -> None:
    event = BabeiEvent.from_dict(
        3,
        {
            "seat": 1,
            "moqie": True,
            "doras": ["4p", "7z"],
        },
    )

    assert event == BabeiEvent(
        action_step=3,
        seat=validate_seat(1),
        moqie=True,
        dora_indicators=(validate_tile("4p"), validate_tile("7z")),
    )


def test_babei_event_rejects_too_many_dora_indicators() -> None:
    with pytest.raises(ValueError, match="at most five"):
        BabeiEvent.from_dict(
            3,
            {
                "seat": 1,
                "moqie": False,
                "doras": ["1m", "2m", "3m", "4m", "5m", "6m"],
            },
        )
