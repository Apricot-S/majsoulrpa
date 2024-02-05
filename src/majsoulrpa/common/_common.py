import datetime
from typing import TypeAlias


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


TimeoutType: TypeAlias = int | float | datetime.timedelta


def to_timedelta(seconds: TimeoutType) -> datetime.timedelta:
    if isinstance(seconds, datetime.timedelta):
        return seconds
    if isinstance(seconds, int | float):
        return datetime.timedelta(seconds=seconds)
    raise TypeError


def timeout_to_deadline(timeout: TimeoutType) -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC) + to_timedelta(timeout)


class Player:
    def __init__(self, account_id: int, name: str) -> None:
        self._account_id = account_id
        self._name = name

    @property
    def account_id(self) -> int:
        return self._account_id

    @property
    def name(self) -> str:
        return self._name
