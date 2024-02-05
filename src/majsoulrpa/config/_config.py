import json
import tomllib
from pathlib import Path
from typing import Any

from jsonschema import RefResolver, validate

_SCHEMA_PATH = Path(__file__).parent
with (_SCHEMA_PATH / "schema.json").open() as _fp:
    _CONFIG_SCHEMA = json.load(_fp)
_REF = RefResolver(_SCHEMA_PATH.as_uri() + "/", _CONFIG_SCHEMA)


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
    validate(config, _CONFIG_SCHEMA, resolver=_REF)

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
    print("")  # noqa: T201

    selection = int(input("Which configuration to use?: "))
    if selection < 0 or selection >= len(config_list):
        msg = f"list index out of range: {selection}"
        raise IndexError(msg)
    return config_list[selection]
