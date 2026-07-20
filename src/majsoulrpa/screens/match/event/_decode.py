from collections.abc import Mapping

from pydantic import JsonValue


def _get_int(data: Mapping[str, JsonValue], name: str) -> int:
    value = data.get(_field_key(name))
    if isinstance(value, bool) or not isinstance(value, int):
        msg = f"{name} must be an int."
        raise TypeError(msg)
    return value


def _get_str(data: Mapping[str, JsonValue], name: str) -> str:
    value = data.get(_field_key(name))
    if not isinstance(value, str):
        msg = f"{name} must be a string."
        raise TypeError(msg)
    return value


def _get_bool(data: Mapping[str, JsonValue], name: str) -> bool:
    value = data.get(_field_key(name))
    if not isinstance(value, bool):
        msg = f"{name} must be a bool."
        raise TypeError(msg)
    return value


def _get_str_list(data: Mapping[str, JsonValue], name: str) -> list[str]:
    value = data.get(_field_key(name))
    if not isinstance(value, list) or not all(
        isinstance(item, str) for item in value
    ):
        msg = f"{name} must be a list of strings."
        raise TypeError(msg)
    return value


def _get_int_list(data: Mapping[str, JsonValue], name: str) -> list[int]:
    value = data.get(_field_key(name))
    if not isinstance(value, list) or not all(
        isinstance(item, int) and not isinstance(item, bool) for item in value
    ):
        msg = f"{name} must be a list of ints."
        raise TypeError(msg)
    return value


def _get_optional_dict(
    data: Mapping[str, JsonValue],
    name: str,
) -> dict[str, JsonValue] | None:
    value = data.get(_field_key(name))
    if value is None:
        return None
    if not isinstance(value, dict):
        msg = f"{name} must be an object or None."
        raise TypeError(msg)
    return value


def _field_key(name: str) -> str:
    return name.rpartition(".")[2]
