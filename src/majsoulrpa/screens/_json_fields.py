from collections.abc import Mapping
from typing import cast

from pydantic import JsonValue

from majsoulrpa.screens._decode_errors import ScreenDecodeError


def _error(name: str, expected: str) -> ScreenDecodeError:
    return ScreenDecodeError(f"{name} must be {expected}.")


def get_int(data: Mapping[str, JsonValue], name: str) -> int:
    value = data.get(name)
    if isinstance(value, bool) or not isinstance(value, int):
        raise _error(name, "an int")
    return value


def get_str(data: Mapping[str, JsonValue], name: str) -> str:
    value = data.get(name)
    if not isinstance(value, str):
        raise _error(name, "a string")
    return value


def get_bool(data: Mapping[str, JsonValue], name: str) -> bool:
    value = data.get(name)
    if not isinstance(value, bool):
        raise _error(name, "a bool")
    return value


def get_list(data: Mapping[str, JsonValue], name: str) -> list[JsonValue]:
    value = data.get(name)
    if not isinstance(value, list):
        raise _error(name, "a list")
    return value


def get_dict(data: Mapping[str, JsonValue], name: str) -> dict[str, JsonValue]:
    value = data.get(name)
    if not isinstance(value, dict):
        raise _error(name, "an object")
    return value


def get_str_list(data: Mapping[str, JsonValue], name: str) -> list[str]:
    value = data.get(name)
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        raise _error(name, "a list of strings")
    return cast("list[str]", value)


def get_int_list(data: Mapping[str, JsonValue], name: str) -> list[int]:
    value = data.get(name)
    if not isinstance(value, list) or not all(
        isinstance(item, int) and not isinstance(item, bool) for item in value
    ):
        raise _error(name, "a list of ints")
    return cast("list[int]", value)


def get_dict_list(
    data: Mapping[str, JsonValue],
    name: str,
) -> list[dict[str, JsonValue]]:
    value = data.get(name)
    if not isinstance(value, list) or not all(
        isinstance(item, dict) for item in value
    ):
        raise _error(name, "a list of objects")
    return cast("list[dict[str, JsonValue]]", value)


def get_optional_dict(
    data: Mapping[str, JsonValue],
    name: str,
) -> dict[str, JsonValue] | None:
    value = data.get(name)
    if value is None:
        return None
    if not isinstance(value, dict):
        raise _error(name, "an object or None")
    return value
