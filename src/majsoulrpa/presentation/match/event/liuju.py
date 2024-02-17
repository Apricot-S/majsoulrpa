# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from majsoulrpa.presentation.exceptions import InconsistentMessageError

from ._base import EventBase


class LiujuEvent(EventBase):
    def __init__(
        self,
        data: Mapping[str, Any],
        timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)

        if data["type"] not in (1, 2, 3, 4):
            raise NotImplementedError(data["type"])
        self._type = (
            None,
            "九種九牌",
            "四風連打",
            "四槓散了",
            "四家立直",
        )[data["type"]]
        if self._type == "九種九牌":
            self._seat = data["seat"]
        else:
            if data["seat"] != 0:
                msg = f'type = {data["type"]}, seat = {data["seat"]}'
                raise InconsistentMessageError(msg)
            self._seat = None

    @property
    def type_(self) -> str:
        assert self._type is not None
        return self._type

    @property
    def seat(self) -> int | None:
        return self._seat
