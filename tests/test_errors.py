from datetime import UTC, datetime
from pathlib import Path

import pytest

from majsoulrpa.screens.errors import ScreenDetectionError


def test_screen_detection_error_exposes_optional_screenshot() -> None:
    error = ScreenDetectionError(
        "detection failed",
        screenshot=b"png-bytes",
    )

    assert str(error) == "detection failed"
    assert error.screenshot() == b"png-bytes"


def test_screen_detection_error_can_have_no_screenshot() -> None:
    error = ScreenDetectionError("detection failed")

    assert error.screenshot() is None


def test_screen_detection_error_saves_screenshot_to_file_path(
    tmp_path: Path,
) -> None:
    error = ScreenDetectionError(
        "detection failed",
        screenshot=b"png-bytes",
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
        screenshot=b"png-bytes",
        created_at=datetime(2026, 7, 8, 1, 2, 3, tzinfo=UTC),
    )

    saved_path = error.save_screenshot(tmp_path)

    assert saved_path == (
        tmp_path / "20260708T010203Z-ScreenDetectionError.png"
    )
    assert saved_path.read_bytes() == b"png-bytes"


def test_screen_detection_error_rejects_save_without_screenshot(
    tmp_path: Path,
) -> None:
    error = ScreenDetectionError("detection failed")

    with pytest.raises(RuntimeError, match="does not have a screenshot"):
        error.save_screenshot(tmp_path)
