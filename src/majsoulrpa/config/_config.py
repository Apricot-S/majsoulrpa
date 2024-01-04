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
    """
    Get the config from a TOML format file.
    If there are multiple configs, select one and input from stdin.

    Parameters
    ----------
    path : str or pathlib.Path
        Path of config file.

    Returns
    -------
    dict[str, Any]
        dict of config.

    Raises
    ------
    FileNotFoundError
        If opening a file fails.
    IndexError
        If there are multiple configs
        and the specified number is outside the range of the list.
    ValueError
        If there are multiple configs
        and non-numeric value is specified.
        If there are multiple configs
        and the config names are duplicated.
    tomllib.TOMLDecodeError
        If config file is invalid TOML document.
    jsonschema.exceptions.ValidationError
        If config is invalid format.
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
