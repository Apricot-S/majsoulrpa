_PORT_SCHEMA = {
    "type": "object",
    "properties": {
        "remote_port": {
            "type": "integer",
            "minimum": 0,
        },
        "proxy_port": {
            "type": "integer",
            "minimum": 0,
        },
        "message_queue_port": {
            "type": "integer",
            "minimum": 0,
        },
    },
}
