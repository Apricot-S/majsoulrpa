import datetime
from enum import Enum
from typing import Literal

from pydantic import BaseModel


class MessageType(Enum):
    NOTIFICATION = 0x01
    REQUEST = 0x02
    RESPONSE = 0x03


class Message(BaseModel):
    request_direction: Literal["inbound", "outbound"]
    name: str
    request: str
    response: str | None
    timestamp: datetime.datetime
