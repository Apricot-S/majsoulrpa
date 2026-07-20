import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match import DapaiEvent


def test_dapai_event_from_dict() -> None:
    event = DapaiEvent.from_dict(
        2,
        {
            "seat": 0,
            "tile": "9s",
            "moqie": False,
            "is_liqi": False,
            "is_wliqi": False,
            "doras": ["3p"],
        },
    )

    assert event == DapaiEvent(
        action_step=2,
        seat=0,
        tile="9s",
        moqie=False,
        liqi=False,
        wliqi=False,
        dora_indicators=("3p",),
    )


@pytest.mark.parametrize(
    "data",
    [
        {
            "seat": 4,
            "tile": "9s",
            "moqie": False,
            "is_liqi": False,
            "is_wliqi": False,
            "doras": [],
        },
        {
            "seat": 0,
            "tile": "9s",
            "moqie": False,
            "is_liqi": True,
            "is_wliqi": True,
            "doras": [],
        },
    ],
)
def test_dapai_event_rejects_invalid_fields(
    data: dict[str, JsonValue],
) -> None:
    with pytest.raises((TypeError, ValueError)):
        DapaiEvent.from_dict(2, data)
