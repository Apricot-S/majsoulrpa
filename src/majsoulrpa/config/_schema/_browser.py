_BROWSER_SCHEMA = {
    "type": "object",
    "properties": {
        "viewport_height": {
            "type": "integer",
            "minimum": 1,
        },
        "initial_position": {
            "type": "object",
            "properties": {
                "left": {
                    "type": "integer",
                },
                "top": {
                    "type": "integer",
                },
            },
        },
        "headless": {
            "type": "boolean",
        },
        "user_data_dir": {
            "type": "string",
        },
    },
}
