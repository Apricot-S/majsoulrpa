# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class ChiPengGangEvent(EventBase):
    def __init__(
        self,
        data: Mapping[str, Any],
        timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        self._seat = data["seat"]
        self._type = ("チー", "ポン", "大明槓")[data["type"]]
        self._from = data["froms"][-1]
        self._tiles = data["tiles"]

    @property
    def seat(self) -> int:
        assert self._seat >= 0
        assert self._seat < 4
        return self._seat

    @property
    def type_(self) -> str:
        return self._type

    @property
    def from_(self) -> str:
        return self._from

    @property
    def tiles(self) -> list[str]:
        return self._tiles
