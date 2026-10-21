import pytest

from majsoulrpa.screens.errors import ScreenError, ScreenInvalidOperationError
from majsoulrpa.screens.room.errors import (
    RoomOperation,
    RoomOperationFailureReason,
    RoomOperationNotAllowedError,
    RoomOperationNotAllowedReason,
    RoomOperationRejectedError,
)

_SCREENSHOT = b"synthetic-private-screenshot"


@pytest.mark.parametrize("reason", list(RoomOperationNotAllowedReason))
def test_not_allowed_preserves_reason_without_exposing_screenshot(
    reason: RoomOperationNotAllowedReason,
) -> None:
    error = RoomOperationNotAllowedError(
        RoomOperation.START_MATCH, reason, _SCREENSHOT
    )

    with pytest.raises(ScreenInvalidOperationError) as caught:
        raise error

    assert caught.value is error
    assert error.operation is RoomOperation.START_MATCH
    assert error.reason is reason
    assert error.screenshot is _SCREENSHOT
    assert error.args == ("Room operation is not allowed: start_match.",)
    assert "synthetic-private-screenshot" not in str(error)
    assert "synthetic-private-screenshot" not in repr(error)


@pytest.mark.parametrize("operation", list(RoomOperation))
def test_rejection_preserves_unknown_code_without_exposing_diagnostics(
    operation: RoomOperation,
) -> None:
    reason = RoomOperationFailureReason.UNRECOGNIZED_ERROR_CODE
    error = RoomOperationRejectedError(
        operation, reason, 987654321, _SCREENSHOT
    )

    with pytest.raises(ScreenError) as caught:
        raise error

    assert caught.value is error
    assert not isinstance(error, ScreenInvalidOperationError)
    assert error.operation is operation
    assert error.reason is reason
    assert error.server_error_code == 987654321
    assert error.screenshot is _SCREENSHOT
    assert error.args == (f"Room operation was rejected: {operation.value}.",)
    for rendered in (str(error), repr(error)):
        assert "synthetic-private-screenshot" not in rendered
        assert "987654321" not in rendered
