import json
import tomllib
from functools import cache
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft7Validator
from referencing import Registry, Resource

_SCHEMA_DIR = Path(__file__).parent


def _retrieve(uri: str) -> Resource:
    parsed_uri = urlparse(uri)
    p = Path(parsed_uri.path).relative_to("/")
    with (_SCHEMA_DIR / p).open() as fp:
        schema = json.load(fp)
    return Resource.from_contents(schema)


@cache
def _get_validator() -> Draft7Validator:
    with (_SCHEMA_DIR / "schema.json").open() as fp:
        config_schema = json.load(fp)
    resource = Resource.from_contents(config_schema)
    registry: Registry = resource @ Registry(retrieve=_retrieve)  # type: ignore[call-arg]
    return Draft7Validator(resource.contents, registry=registry)


def get_config(path: str | Path) -> dict[str, Any]:
    """Gets the configuration from a TOML format file.

    If there are multiple configurations, select one with input from
    `stdin`.

    Args:
        path: A path of configuration file.

    Returns:
        A dict containing the configuration settings.

    Raises:
        FileNotFoundError: Failed to open file.
        IndexError: A specified number was outside the range of the list
            when selecting one from multiple configurations.
        ValueError: A non-numeric value is specified when selecting one
            from multiple configurations, or a configuration name is
            duplicated.
        tomllib.TOMLDecodeError: A file was invalid TOML document.
        jsonschema.ValidationError: The configuration was not in
            the correct format.
    """
    if isinstance(path, str):
        path = Path(path)

    with path.open("rb") as fp:
        config = tomllib.load(fp)
    _get_validator().validate(config)

    config_list = next(iter(config.values()))
    if not isinstance(config_list, list):
        return config

    if len(config_list) == 1:
        return config_list[0]

    name_list = [c["name"] for c in config_list]
    duplicate_names = {n for n in name_list if name_list.count(n) > 1}
    if duplicate_names:
        msg = f"{', '.join(duplicate_names)}: Duplicate config names."
        raise ValueError(msg)

    for i, c in enumerate(config_list):
        name = c["name"]
        print(f"{i}: {name}")  # noqa: T201
    print()  # noqa: T201

    selection = int(input("Which configuration to use?: "))
    if selection < 0 or selection >= len(config_list):
        msg = f"list index out of range: {selection}"
        raise IndexError(msg)
    return config_list[selection]
