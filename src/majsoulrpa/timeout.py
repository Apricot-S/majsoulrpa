"""Functionality for handling timeout duration."""

import datetime

type TimeoutType = int | float | datetime.timedelta
"""A type representing timeout duration.

    The unit is seconds.
"""


def to_timedelta(seconds: TimeoutType) -> datetime.timedelta:
    """Converts `TimeoutType` to `datetime.timedelta`.

    Args:
        seconds: Timeout duration in seconds.

    Returns:
        A `datetime.timedelta` object that represents the same timeout
            duration as the input `seconds`.
    """
    if isinstance(seconds, datetime.timedelta):
        return seconds
    if isinstance(seconds, int | float):
        return datetime.timedelta(seconds=seconds)

    msg = f"{seconds} is not `TimeoutType`."
    raise TypeError(msg)


def timeout_to_deadline(timeout: TimeoutType) -> datetime.datetime:
    """Converts timeout duration to a deadline from the current time.

    Args:
        timeout: Timeout duration in seconds.

    Returns:
        A deadline from the current time.
    """
    return datetime.datetime.now(datetime.UTC) + to_timedelta(timeout)
