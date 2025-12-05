from ipaddress import IPv4Address, IPv6Address, ip_address
from typing import NewType

from majsoulrpa.exceptions import UserInputError

MIN_USER_PORT = 1024
MAX_USER_PORT = 49151

UserPort = NewType("UserPort", int)


def parse_ip_address(raw_ip_address: str) -> IPv4Address | IPv6Address:
    try:
        return ip_address(raw_ip_address)
    except ValueError as e:
        msg = "invalid IP address"
        raise UserInputError(msg) from e


def validate_user_port(port: int) -> UserPort:
    """Validates port is in the range of user ports (1024-49151).

    Args:
        port: A port number to validate.

    Returns:
        The validated port number.

    Raises:
        UserInputError: A port was not in the range of user ports.
    """
    if not (MIN_USER_PORT <= port <= MAX_USER_PORT):
        msg = "port must be in the range 1024-49151."
        raise UserInputError(msg)
    return UserPort(port)


def make_endpoint(address: IPv4Address | IPv6Address, port: UserPort) -> str:
    if address.version == 6:  # noqa: PLR2004
        return f"[{address}]:{port}"

    return f"{address}:{port}"
