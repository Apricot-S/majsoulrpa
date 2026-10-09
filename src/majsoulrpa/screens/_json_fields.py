from collections.abc import Mapping
from typing import cast

from pydantic import JsonValue


class JsonFieldDecodeError(TypeError):
    """Invalid JSON field; diagnostics contain no input values."""


def _error(label: str, expected: str) -> JsonFieldDecodeError:
    return JsonFieldDecodeError(f"{label} must be {expected}.")


def get_int(data: Mapping[str, JsonValue], key: str, *, label: str) -> int:
    value = data.get(key)
    if isinstance(value, bool) or not isinstance(value, int):
        raise _error(label, "an int")
    return value


def get_str(data: Mapping[str, JsonValue], key: str, *, label: str) -> str:
    value = data.get(key)
    if not isinstance(value, str):
        raise _error(label, "a string")
    return value


def get_bool(data: Mapping[str, JsonValue], key: str, *, label: str) -> bool:
    value = data.get(key)
    if not isinstance(value, bool):
        raise _error(label, "a bool")
    return value


def get_list(
    data: Mapping[str, JsonValue],
    key: str,
    *,
    label: str,
) -> list[JsonValue]:
    value = data.get(key)
    if not isinstance(value, list):
        raise _error(label, "a list")
    return value


def get_dict(
    data: Mapping[str, JsonValue],
    key: str,
    *,
    label: str,
) -> dict[str, JsonValue]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise _error(label, "an object")
    return value


def get_str_list(
    data: Mapping[str, JsonValue],
    key: str,
    *,
    label: str,
) -> list[str]:
    value = data.get(key)
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise _error(label, "a list of strings")
    return cast("list[str]", value)


def get_int_list(
    data: Mapping[str, JsonValue],
    key: str,
    *,
    label: str,
) -> list[int]:
    value = data.get(key)
    if not isinstance(value, list) or not all(
        isinstance(item, int) and not isinstance(item, bool) for item in value
    ):
        raise _error(label, "a list of ints")
    return cast("list[int]", value)


def get_dict_list(
    data: Mapping[str, JsonValue],
    key: str,
    *,
    label: str,
) -> list[dict[str, JsonValue]]:
    value = data.get(key)
    if not isinstance(value, list) or not all(
        isinstance(item, dict) for item in value
    ):
        raise _error(label, "a list of objects")
    return cast("list[dict[str, JsonValue]]", value)


def get_optional_dict(
    data: Mapping[str, JsonValue],
    key: str,
    *,
    label: str,
) -> dict[str, JsonValue] | None:
    value = data.get(key)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise _error(label, "an object or None")
    return value
