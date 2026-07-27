from collections.abc import Callable, Mapping

import pytest
from pydantic import JsonValue

from majsoulrpa.screens.match._decode import (
    _get_bool,
    _get_int,
    _get_int_list,
    _get_str,
    _get_str_list,
)


@pytest.mark.parametrize(
    ("getter", "value", "expected"),
    [
        (_get_int, 1, 1),
        (_get_str, "1m", "1m"),
        (_get_bool, True, True),
        (_get_int_list, [1, 2], [1, 2]),
        (_get_str_list, ["1m", "2m"], ["1m", "2m"]),
    ],
)
def test_event_field_getter_uses_qualified_field_name(
    getter: Callable[[Mapping[str, JsonValue], str], object],
    value: JsonValue,
    expected: object,
) -> None:
    assert getter({"field": value}, "ActionExample.field") == expected


def test_event_field_getter_reports_qualified_field_name() -> None:
    with pytest.raises(
        TypeError,
        match=r"^ActionExample\.field must be an int\.$",
    ):
        _get_int({"field": True}, "ActionExample.field")
