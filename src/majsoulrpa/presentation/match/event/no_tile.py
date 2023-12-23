# ruff: noqa: PLR2004, S101
import datetime
from collections.abc import Mapping
from typing import Any

from ._base import EventBase


class NoTileEvent(EventBase):
    def __init__(
        self,
        data: Mapping[str, Any],  # noqa: ARG002
        timestamp: datetime.datetime,
    ) -> None:
        super().__init__(timestamp)
        # TODO
