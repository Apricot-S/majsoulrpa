import datetime

type TimeoutType = int | float | datetime.timedelta


def to_timedelta(seconds: TimeoutType) -> datetime.timedelta:
    if isinstance(seconds, datetime.timedelta):
        return seconds
    if isinstance(seconds, int | float):
        return datetime.timedelta(seconds=seconds)
    raise TypeError


def timeout_to_deadline(timeout: TimeoutType) -> datetime.datetime:
    return datetime.datetime.now(datetime.UTC) + to_timedelta(timeout)
