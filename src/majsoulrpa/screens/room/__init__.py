from typing import TYPE_CHECKING

from majsoulrpa.screens.room.errors import (
    RoomOperation,
    RoomOperationFailureReason,
    RoomOperationNotAllowedError,
    RoomOperationNotAllowedReason,
    RoomOperationRejectedError,
)
from majsoulrpa.screens.room.state import RoomPlayer, RoomState, RoomStatus

if TYPE_CHECKING:
    from majsoulrpa.screens.room.screen import RoomScreen

__all__ = [
    "RoomOperation",
    "RoomOperationFailureReason",
    "RoomOperationNotAllowedError",
    "RoomOperationNotAllowedReason",
    "RoomOperationRejectedError",
    "RoomPlayer",
    "RoomScreen",
    "RoomState",
    "RoomStatus",
]


def __getattr__(name: str) -> object:
    if name != "RoomScreen":
        msg = f"module {__name__!r} has no attribute {name!r}"
        raise AttributeError(msg)

    from majsoulrpa.screens.room.screen import RoomScreen  # noqa: PLC0415

    globals()[name] = RoomScreen
    return RoomScreen
