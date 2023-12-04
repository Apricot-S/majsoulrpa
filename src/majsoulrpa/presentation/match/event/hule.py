# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class HuleEvent(EventBase):

    def __init__(
        self, data: Mapping[str, Any], timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        # TODO: data['hules']
        self._old_scores = data["old_scores"]
        self._delta_scores = data["delta_scores"]
        self._scores = data["scores"]


    @property
    def old_scores(self) -> list[int]:
        assert len(self._old_scores) in (4, 3)
        return self._old_scores

    @property
    def delta_scores(self) -> list[int]:
        assert len(self._delta_scores) in (4, 3)
        return self._delta_scores

    @property
    def scores(self) -> list[int]:
        assert len(self._scores) in (4, 3)
        return self._scores
