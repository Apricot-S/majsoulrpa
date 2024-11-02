_AUTHENTICATION_IMAP_SCHEMA = {
    "type": "object",
    "required": [
        "method",
        "email_address",
        "imap_server",
        "password",
        "mail_folder",
    ],
    "properties": {
        "method": {
            "const": "imap",
        },
        "email_address": {
            "type": "string",
        },
        "imap_server": {
            "type": "string",
        },
        "password": {
            "type": "string",
        },
        "mail_folder": {
            "type": "string",
        },
    },
}
