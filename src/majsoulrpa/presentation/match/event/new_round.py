# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class NewRoundEvent(EventBase):
    def __init__(
        self,
        data: Mapping[str, Any],
        timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        self._chang = data["chang"]
        self._ju = data["ju"]
        self._ben = data["ben"]
        self._liqibang = data["liqibang"]
        self._dora_indicators = data["doras"]
        self._left_tile_count = data["left_tile_count"]
        self._scores = data["scores"]
        self._shoupai = data["tiles"][:13]
        if len(data["tiles"]) == 14:
            self._zimopai = data["tiles"][13]
        else:
            self._zimopai = None

    @property
    def chang(self) -> int:
        assert self._chang >= 0
        assert self._chang < 3
        return self._chang

    @property
    def ju(self) -> int:
        assert self._ju >= 0
        assert self._ju < 4
        return self._ju

    @property
    def ben(self) -> int:
        assert self._ben >= 0
        return self._ben

    @property
    def liqibang(self) -> int:
        assert self._liqibang >= 0
        return self._liqibang

    @property
    def dora_indicators(self) -> list[str]:
        assert len(self._dora_indicators) >= 1
        assert len(self._dora_indicators) <= 5
        return self._dora_indicators

    @property
    def left_tile_count(self) -> int:
        assert self._left_tile_count < 70
        assert self._left_tile_count >= 0
        return self._left_tile_count

    @property
    def scores(self) -> list[int]:
        assert len(self._scores) in (4, 3)
        return self._scores

    @property
    def shoupai(self) -> list[str]:
        assert len(self._shoupai) == 13
        return self._shoupai

    @property
    def zimopai(self) -> str | None:
        return self._zimopai
