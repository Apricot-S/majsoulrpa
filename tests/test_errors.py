from datetime import UTC, datetime
from pathlib import Path

from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenDetectionTimeoutError,
    ScreenError,
    ScreenInvalidArgumentError,
    ScreenInvalidOperationError,
    ScreenStaleError,
)


def test_screen_detection_error_exposes_screenshot() -> None:
    error = ScreenDetectionError(
        "detection failed",
        b"png-bytes",
    )

    assert str(error) == "detection failed"
    assert error.screenshot == b"png-bytes"
    assert isinstance(error, ScreenError)


def test_screen_invalid_argument_error_is_screen_value_error() -> None:
    error = ScreenInvalidArgumentError(
        "invalid screen API argument",
        b"png-bytes",
    )

    assert str(error) == "invalid screen API argument"
    assert error.screenshot == b"png-bytes"
    assert isinstance(error, ScreenError)
    assert isinstance(error, ValueError)


def test_screen_invalid_operation_error_is_screen_error() -> None:
    error = ScreenInvalidOperationError(
        "invalid screen API operation",
        b"png-bytes",
    )

    assert str(error) == "invalid screen API operation"
    assert error.screenshot == b"png-bytes"
    assert isinstance(error, ScreenError)


def test_screen_stale_error_is_invalid_operation_error() -> None:
    error = ScreenStaleError("screen is stale", b"png-bytes")

    assert error.screenshot == b"png-bytes"
    assert isinstance(error, ScreenInvalidOperationError)


def test_screen_detection_timeout_error_is_timeout_error() -> None:
    error = ScreenDetectionTimeoutError("detection timed out", b"png-bytes")

    assert isinstance(error, ScreenError)
    assert isinstance(error, TimeoutError)


def test_screen_detection_error_saves_screenshot_to_file_path(
    tmp_path: Path,
) -> None:
    error = ScreenDetectionError(
        "detection failed",
        b"png-bytes",
        created_at=datetime(2026, 7, 8, 1, 2, 3, tzinfo=UTC),
    )
    screenshot_path = tmp_path / "failure.png"

    saved_path = error.save_screenshot(screenshot_path)

    assert saved_path == screenshot_path
    assert screenshot_path.read_bytes() == b"png-bytes"


def test_screen_detection_error_saves_screenshot_to_directory(
    tmp_path: Path,
) -> None:
    error = ScreenDetectionError(
        "detection failed",
        b"png-bytes",
        created_at=datetime(2026, 7, 8, 1, 2, 3, tzinfo=UTC),
    )

    saved_path = error.save_screenshot(tmp_path)

    assert saved_path == (
        tmp_path / "20260708T010203Z-ScreenDetectionError.png"
    )
    assert saved_path.read_bytes() == b"png-bytes"


def test_screen_detection_timeout_error_saves_screenshot_to_directory(
    tmp_path: Path,
) -> None:
    error = ScreenDetectionTimeoutError(
        "detection timed out",
        b"png-bytes",
        created_at=datetime(2026, 7, 8, 1, 2, 3, tzinfo=UTC),
    )

    saved_path = error.save_screenshot(tmp_path)

    assert saved_path == (
        tmp_path / "20260708T010203Z-ScreenDetectionTimeoutError.png"
    )
    assert saved_path.read_bytes() == b"png-bytes"


def test_screen_invalid_argument_error_saves_screenshot_to_directory(
    tmp_path: Path,
) -> None:
    error = ScreenInvalidArgumentError(
        "invalid screen API argument",
        b"png-bytes",
        created_at=datetime(2026, 7, 8, 1, 2, 3, tzinfo=UTC),
    )

    saved_path = error.save_screenshot(tmp_path)

    assert saved_path == (
        tmp_path / "20260708T010203Z-ScreenInvalidArgumentError.png"
    )
    assert saved_path.read_bytes() == b"png-bytes"


def test_screen_invalid_operation_error_saves_screenshot_to_directory(
    tmp_path: Path,
) -> None:
    error = ScreenInvalidOperationError(
        "invalid screen API operation",
        b"png-bytes",
        created_at=datetime(2026, 7, 8, 1, 2, 3, tzinfo=UTC),
    )

    saved_path = error.save_screenshot(tmp_path)

    assert saved_path == (
        tmp_path / "20260708T010203Z-ScreenInvalidOperationError.png"
    )
    assert saved_path.read_bytes() == b"png-bytes"
