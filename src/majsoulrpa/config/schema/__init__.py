from typing import Final

from ._authentication import _AUTHENTICATION_SCHEMA
from ._browser import _BROWSER_SCHEMA
from ._port import _PORT_SCHEMA

_CONFIG_SCHEMA: Final = {
    "type": "object",
    "properties": {
        "type": "array",
        "items": {
            "type": "object",
            "required": [
                "name",
            ],
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
    },
}
