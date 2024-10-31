from ._imap import _AUTHENTICATION_IMAP_SCHEMA
from ._s3 import _AUTHENTICATION_S3_SCHEMA

_AUTHENTICATION_SCHEMA = {
    "oneOf": [
        {
            "required": [
                "email_address",
            ],
            "properties": {
                "email_address": {
                    "type": "string",
                },
            },
            "additionalProperties": False,
        },
        _AUTHENTICATION_IMAP_SCHEMA,
        _AUTHENTICATION_S3_SCHEMA,
    ],
}
