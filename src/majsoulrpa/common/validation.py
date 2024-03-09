def validate_user_port(port: int) -> None:
    """Validates port is in the range of user ports (1024-49151).

    Args:
        port: A port number to validate.

    Raises:
        ValueError: A port was not in the range of user ports.
    """
    if (port < 1024) or (port > 49151):  # noqa: PLR2004
        msg = "The port must be in the range 1024-49151."
        raise ValueError(msg)
