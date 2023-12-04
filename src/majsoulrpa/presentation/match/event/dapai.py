# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class DapaiEvent(EventBase):

    def __init__(
        self, data: Mapping[str, Any], timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        self._seat = data["seat"]
        self._tile = data["tile"]
        self._moqie = data["moqie"]
        self._liqi = data["is_liqi"]
        self._wliqi = data["is_wliqi"]

    @property
    def seat(self) -> int:
        assert self._seat >= 0
        assert self._seat < 4
        return self._seat

    @property
    def tile(self) -> str:
        return self._tile

    @property
    def moqie(self) -> bool:
        return self._moqie

    @property
    def liqi(self) -> bool:
        return self._liqi

    @property
    def wliqi(self) -> bool:
        return self._wliqi
