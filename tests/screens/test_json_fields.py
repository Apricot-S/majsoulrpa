from collections.abc import Callable, Mapping

import pytest
from pydantic import JsonValue

from majsoulrpa.screens._json_fields import (
    get_bool,
    get_dict,
    get_dict_list,
    get_int,
    get_int_list,
    get_list,
    get_optional_dict,
    get_str,
    get_str_list,
)
from majsoulrpa.screens.errors import MessageDecodeError


@pytest.mark.parametrize(
    ("getter", "value"),
    [
        (get_int, 7),
        (get_str, "synthetic"),
        (get_bool, False),
        (get_list, [None]),
        (get_dict, {}),
        (get_int_list, [1, 2]),
        (get_str_list, ["synthetic"]),
        (get_dict_list, [{}]),
        (get_optional_dict, {}),
    ],
)
def test_getter_returns_value_without_copying(
    getter: Callable[..., object],
    value: JsonValue,
) -> None:
    assert getter({"key": value}, "key") is value


@pytest.mark.parametrize(
    "data",
    [{}, {"key": None}, {"key": True}, {"key": "synthetic-private-value"}],
)
def test_integer_rejects_missing_null_boolean_and_text(
    data: Mapping[str, JsonValue],
) -> None:
    with pytest.raises(
        MessageDecodeError, match=r"^key must be an int\.$"
    ) as caught:
        get_int(data, "key")
    assert "synthetic-private-value" not in str(caught.value)
    assert "synthetic-private-value" not in repr(caught.value)


@pytest.mark.parametrize("data", [{}, {"key": None}])
def test_optional_object_allows_missing_and_null(
    data: Mapping[str, JsonValue],
) -> None:
    assert get_optional_dict(data, "key") is None


@pytest.mark.parametrize(
    "getter",
    [
        get_str,
        get_bool,
        get_list,
        get_dict,
        get_int_list,
        get_str_list,
        get_dict_list,
    ],
)
@pytest.mark.parametrize(
    "data", [{}, {"key": None}, {"key": "synthetic-private-value"}]
)
def test_required_fields_reject_missing_null_and_wrong_type(
    getter: Callable[..., object],
    data: Mapping[str, JsonValue],
) -> None:
    # get_str needs a non-string for this wrong-type case.
    if getter is get_str and data.get("key") == "synthetic-private-value":
        data = {"key": 7}
    with pytest.raises(MessageDecodeError, match=r"key") as caught:
        getter(data, "key")
    assert "synthetic-private-value" not in str(caught.value)
    assert "synthetic-private-value" not in repr(caught.value)


@pytest.mark.parametrize(
    ("getter", "value"),
    [
        (get_int_list, [1, True]),
        (get_str_list, ["synthetic-private-value", 7]),
        (get_dict_list, [{}, "synthetic-private-value"]),
        (get_optional_dict, "synthetic-private-value"),
    ],
)
def test_typed_lists_and_optional_object_reject_invalid_values(
    getter: Callable[..., object],
    value: JsonValue,
) -> None:
    with pytest.raises(MessageDecodeError, match=r"key") as caught:
        getter({"key": value}, "key")
    assert "synthetic-private-value" not in str(caught.value)
    assert "synthetic-private-value" not in repr(caught.value)
