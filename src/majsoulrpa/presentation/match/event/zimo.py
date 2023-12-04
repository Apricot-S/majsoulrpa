# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class ZimoEvent(EventBase):

    def __init__(
        self, data: Mapping[str, Any], timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        self._seat = data["seat"]
        if data["tile"] != "":
            self._tile = data["tile"]
        else:
            self._tile = None
        self._left_tile_count = data["left_tile_count"]

    @property
    def seat(self) -> int:
        assert self._seat >= 0
        assert self._seat < 4
        return self._seat

    @property
    def tile(self) -> str | None:
        return self._tile

    @property
    def left_tile_count(self) -> int:
        assert self._left_tile_count < 70
        assert self._left_tile_count >= 0
        return self._left_tile_count
