import datetime
from collections.abc import Callable

type Clock = Callable[[], datetime.datetime]


def utc_now() -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC)
