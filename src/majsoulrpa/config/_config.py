import tomllib
from functools import cache
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

from ._schema import _CONFIG_FILE_SCHEMA


@cache
def _get_validator() -> Draft202012Validator:
    return Draft202012Validator(_CONFIG_FILE_SCHEMA)


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
            from multiple configurations.
        tomllib.TOMLDecodeError: A file was invalid TOML document.
        jsonschema.ValidationError: The configuration was not in
            the correct format.
    """
    if isinstance(path, str):
        path = Path(path)

    with path.open("rb") as fp:
        config = tomllib.load(fp)
    _get_validator().validate(config)

    config_list = config.get("majsoulrpa")

    if config_list is None:
        return {}

    if len(config_list) == 1:
        return config_list[0]

    for i, c in enumerate(config_list):
        name = c.get("name", "")
        print(f"{i}: {name}")  # noqa: T201
    print()  # noqa: T201

    selection = int(input("Which configuration to use?: "))
    if selection < 0 or selection >= len(config_list):
        msg = f"list index out of range: {selection}"
        raise IndexError(msg)
    return config_list[selection]
