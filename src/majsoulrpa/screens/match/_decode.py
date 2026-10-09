from collections.abc import Mapping

from pydantic import JsonValue

from majsoulrpa.screens._json_fields import (
    get_bool,
    get_dict_list,
    get_int,
    get_int_list,
    get_optional_dict,
    get_str,
    get_str_list,
)


def _get_int(data: Mapping[str, JsonValue], name: str) -> int:
    return get_int(data, _field_key(name), label=name)


def _get_str(data: Mapping[str, JsonValue], name: str) -> str:
    return get_str(data, _field_key(name), label=name)


def _get_bool(data: Mapping[str, JsonValue], name: str) -> bool:
    return get_bool(data, _field_key(name), label=name)


def _get_str_list(data: Mapping[str, JsonValue], name: str) -> list[str]:
    return get_str_list(data, _field_key(name), label=name)


def _get_int_list(data: Mapping[str, JsonValue], name: str) -> list[int]:
    return get_int_list(data, _field_key(name), label=name)


def _get_dict_list(
    data: Mapping[str, JsonValue],
    name: str,
) -> list[dict[str, JsonValue]]:
    return get_dict_list(data, _field_key(name), label=name)


def _get_optional_dict(
    data: Mapping[str, JsonValue],
    name: str,
) -> dict[str, JsonValue] | None:
    return get_optional_dict(data, _field_key(name), label=name)


def _field_key(name: str) -> str:
    return name.rpartition(".")[2]
