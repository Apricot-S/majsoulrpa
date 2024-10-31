from typing import Final

from ._authentication import _AUTHENTICATION_SCHEMA
from ._browser import _BROWSER_SCHEMA
from ._port import _PORT_SCHEMA

_CONFIG_SCHEMA: Final = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
            },
            "authentication": _AUTHENTICATION_SCHEMA,
            "remote_host": {
                "type": "string",
            },
            "port": _PORT_SCHEMA,
            "browser": _BROWSER_SCHEMA,
        },
        "additionalProperties": True,
    },
}

_CONFIG_FILE_SCHEMA: Final = {
    "type": "object",
    "properties": {
        "majsoulrpa": _CONFIG_SCHEMA,
    },
    "additionalProperties": True,
}
