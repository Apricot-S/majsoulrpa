import datetime as dt
from collections.abc import Callable

type Clock = Callable[[], dt.datetime]


def utc_now() -> dt.datetime:
    return dt.datetime.now(dt.UTC)
