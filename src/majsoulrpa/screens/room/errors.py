from enum import Enum, StrEnum

from majsoulrpa.screens.errors import ScreenError


class RoomOperation(StrEnum):
    LEAVE = "leave"


class RoomOperationFailureReason(Enum):
    UNRECOGNIZED_ERROR_CODE = -1


class RoomOperationRejectedError(ScreenError):
    def __init__(
        self,
        operation: RoomOperation,
        reason: RoomOperationFailureReason,
        server_error_code: int,
        screenshot: bytes,
    ) -> None:
        super().__init__(
            f"Room operation was rejected: {operation.value}.",
            screenshot,
        )
        self._operation = operation
        self._reason = reason
        self._server_error_code = server_error_code

    @property
    def operation(self) -> RoomOperation:
        return self._operation

    @property
    def reason(self) -> RoomOperationFailureReason:
        return self._reason

    @property
    def server_error_code(self) -> int:
        return self._server_error_code


__all__ = [
    "RoomOperation",
    "RoomOperationFailureReason",
    "RoomOperationRejectedError",
]
