import tomllib
from pathlib import Path
from typing import Any

_config: dict[str, Any] | None = None


def _validate_config(config: dict[str, Any]) -> None:
    def validate_dict(dict_: dict[str, Any], key: str, type_: type) -> None:
        if key not in dict_:
            msg = f"'{key}' is not found."
            raise KeyError(msg)
        if not isinstance(dict_[key], type_):
            msg = f"'{key}' is not {type_}."
            raise TypeError(msg)

    validate_dict(config, "email_address", str)
    validate_dict(config, "viewport_height", int)
    validate_dict(config, "initial_position", dict)
    validate_dict(config["initial_position"], "left", int)
    validate_dict(config["initial_position"], "top", int)


def get_config(path: str | Path) -> dict[str, Any]:
    """Get config from file.

    Parameters
    ----------
    path : str | pathlib.Path
        Path of config file.

    Returns
    -------
    dict[str, Any]
        dict of config.

    Raises
    ------
    RuntimeError
        If loading config fails.
    KeyError
        If config item is not found.
    TypeError
        If config is invalid type.
    tomllib.TOMLDecodeError
        If config file is invalid TOML document.
    """
    global _config  # noqa: PLW0603
    if _config is not None:
        return _config

    if isinstance(path, str):
        path = Path(path)

    if not path.exists():
        msg = f"{path}: Does not exist."
        raise RuntimeError(msg)
    if not path.is_file():
        msg = f"{path}: Is not a file."
        raise RuntimeError(msg)

    with path.open("rb") as fp:
        config = tomllib.load(fp)

    _validate_config(config)
    _config = config

    return config
