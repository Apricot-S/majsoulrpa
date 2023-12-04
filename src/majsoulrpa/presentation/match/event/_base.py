import datetime


class EventBase:

    def __init__(self, timestamp: datetime.datetime) -> None:
        self._timestamp = timestamp

    @property
    def timestamp(self) -> datetime.datetime:
        return self._timestamp
