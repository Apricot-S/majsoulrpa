from enum import Enum, StrEnum

from majsoulrpa.screens.errors import ScreenError, ScreenInvalidOperationError


class RoomOperation(StrEnum):
    ADD_AI = "add_ai"
    LEAVE = "leave"


class RoomOperationFailureReason(Enum):
    UNRECOGNIZED_ERROR_CODE = -1


class RoomOperationNotAllowedReason(StrEnum):
    NOT_HOST = "not_host"
    ROOM_FULL = "room_full"


class RoomOperationNotAllowedError(ScreenInvalidOperationError):
    def __init__(
        self,
        operation: RoomOperation,
        reason: RoomOperationNotAllowedReason,
        screenshot: bytes,
    ) -> None:
        super().__init__(
            f"Room operation is not allowed: {operation.value}.",
            screenshot,
        )
        self._operation = operation
        self._reason = reason

    @property
    def operation(self) -> RoomOperation:
        return self._operation

    @property
    def reason(self) -> RoomOperationNotAllowedReason:
        return self._reason


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
    "RoomOperationNotAllowedError",
    "RoomOperationNotAllowedReason",
    "RoomOperationRejectedError",
]
