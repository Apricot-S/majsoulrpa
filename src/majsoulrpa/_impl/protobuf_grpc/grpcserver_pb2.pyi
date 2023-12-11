from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class NoneResponse(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Message(_message.Message):
    __slots__ = ["content"]
    CONTENT_FIELD_NUMBER: _ClassVar[int]
    content: bytes
    def __init__(self, content: _Optional[bytes] = ...) -> None: ...

class Timeout(_message.Message):
    __slots__ = ["seconds"]
    SECONDS_FIELD_NUMBER: _ClassVar[int]
    seconds: float
    def __init__(self, seconds: _Optional[float] = ...) -> None: ...
