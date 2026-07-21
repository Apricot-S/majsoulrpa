import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match.operation._decode import (
    decode_operation_specification,
)


def test_decode_dapai_operation_specification() -> None:
    specification = decode_operation_specification(
        {
            "operation": {
                "seat": 0,
                "operation_list": [
                    {
                        "type": 1,
                        "combination": ["5m", "7z"],
                        "change_tiles": [],
                        "change_tile_states": [],
                        "gap_type": 0,
                    }
                ],
                "time_add": 20000,
                "time_fixed": 5000,
            }
        }
    )

    assert specification is not None
    assert specification.time_fixed_ms == 5000
    assert specification.time_add_ms == 20000
    [operation] = specification.operations
    assert operation.forbidden_tiles == ("5m", "7z")


@pytest.mark.parametrize(
    "data",
    [
        {},
        {
            "operation": {
                "operation_list": [],
                "time_add": 0,
                "time_fixed": 0,
            }
        },
    ],
)
def test_decode_absent_or_empty_operation_as_none(
    data: dict[str, JsonValue],
) -> None:
    assert decode_operation_specification(data) is None


@pytest.mark.parametrize(
    "operation",
    [
        [],
        {"operation_list": [], "time_add": True, "time_fixed": 0},
        {"operation_list": [], "time_add": 0, "time_fixed": -1},
        {"operation_list": {}, "time_add": 0, "time_fixed": 0},
        {
            "operation_list": [{"type": True, "combination": []}],
            "time_add": 0,
            "time_fixed": 0,
        },
        {
            "operation_list": [{"type": 1, "combination": ["1x"]}],
            "time_add": 0,
            "time_fixed": 0,
        },
        {
            "operation_list": [{"type": 2, "combination": ["1m|2m"]}],
            "time_add": 0,
            "time_fixed": 0,
        },
        {
            "operation_list": [{"type": 99, "combination": []}],
            "time_add": 0,
            "time_fixed": 0,
        },
    ],
)
def test_decode_operation_rejects_invalid_or_unsupported_fields(
    operation: JsonValue,
) -> None:
    with pytest.raises((TypeError, ValueError)):
        decode_operation_specification({"operation": operation})
