import datetime
from typing import Literal

from pydantic import BaseModel


class Message(BaseModel):
    request_direction: Literal["inbound", "outbound"]
    name: str
    request: str
    response: str | None
    timestamp: datetime.datetime
