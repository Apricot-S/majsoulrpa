_AUTHENTICATION_S3_SCHEMA = {
    "type": "object",
    "required": [
        "method",
        "email_address",
        "bucket_name",
        "key_prefix",
    ],
    "properties": {
        "method": {
            "const": "s3",
        },
        "email_address": {
            "type": "string",
        },
        "bucket_name": {
            "type": "string",
        },
        "key_prefix": {
            "type": "string",
        },
    },
    "additionalProperties": {
        "aws_profile": {
            "type": "string",
        },
    },
}
