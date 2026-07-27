import pytest

from majsoulrpa.screens.match import (
    JiagangEvent,
    validate_seat,
    validate_tile,
)


@pytest.mark.parametrize(
    ("added", "consumed"),
    [
        ("0m", ("5m", "5m", "5m")),
        ("5m", ("0m", "5m", "5m")),
        ("0p", ("5p", "5p", "5p")),
        ("5p", ("0p", "5p", "5p")),
        ("0s", ("5s", "5s", "5s")),
        ("5s", ("0s", "5s", "5s")),
        ("5z", ("5z", "5z", "5z")),
        ("7z", ("7z", "7z", "7z")),
    ],
)
def test_jiagang_event_preserves_added_and_canonicalizes_consumed(
    added: str,
    consumed: tuple[str, str, str],
) -> None:
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
        consumed=(
            validate_tile(consumed[0]),
            validate_tile(consumed[1]),
            validate_tile(consumed[2]),
        ),
        dora_indicators=(validate_tile("4p"), validate_tile("7z")),
    )


def test_jiagang_event_rejects_noncanonical_consumed() -> None:
    with pytest.raises(ValueError, match="canonical jiagang"):
        JiagangEvent(
            action_step=3,
            seat=validate_seat(1),
            consumed=(
                validate_tile("5m"),
                validate_tile("5m"),
                validate_tile("5m"),
            ),
            added=validate_tile("5m"),
            dora_indicators=(),
        )


@pytest.mark.parametrize("type_", [3, 4])
def test_jiagang_event_rejects_other_action_types(type_: int) -> None:
    with pytest.raises(ValueError, match="identify jiagang"):
        JiagangEvent.from_dict(
            3,
            {"seat": 1, "type": type_, "tiles": "7z", "doras": []},
        )
