# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class BabeiEvent(EventBase):

    def __init__(
        self, data: Mapping[str, Any], timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        self._seat = data["seat"]

    @property
    def seat(self) -> int:
        assert self._seat >= 0
        assert self._seat < 3
        return self._seat
