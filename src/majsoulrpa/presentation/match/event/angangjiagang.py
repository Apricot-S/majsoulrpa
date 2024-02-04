# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class AngangJiagangEvent(EventBase):
    def __init__(
        self,
        data: Mapping[str, Any],
        timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        self._seat = data["seat"]
        self._type = (None, None, "加槓", "暗槓")[data["type"]]
        self._tile = data["tiles"]

    @property
    def seat(self) -> int:
        assert self._seat >= 0
        assert self._seat < 4
        return self._seat

    @property
    def type_(self) -> str:
        assert self._type in ("加槓", "暗槓")
        return self._type

    @property
    def tile(self) -> str:
        return self._tile
