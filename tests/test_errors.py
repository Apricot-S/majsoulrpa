from datetime import UTC, datetime, timedelta, timezone, tzinfo
from pathlib import Path

import pytest

import majsoulrpa.screens.errors as screen_errors
from majsoulrpa.screens.errors import (
    ScreenDetectionError,
    ScreenDetectionTimeoutError,
    ScreenError,
    ScreenInconsistentMessageError,
    ScreenInvalidArgumentError,
    ScreenInvalidOperationError,
    ScreenNotImplementedOperationError,
    ScreenStaleError,
    ScreenUnexpectedStateError,
)


class UndefinedOffset(tzinfo):
    def utcoffset(self, _dt: datetime | None) -> None:
        return None

    def dst(self, _dt: datetime | None) -> None:
        return None

    def tzname(self, _dt: datetime | None) -> None:
        return None


class TestScreenshotTimestamp:
    @pytest.mark.parametrize(
        "created_at",
        [
            datetime(2026, 7, 8, 1, 2, 3),  # noqa: DTZ001 -- invalid input
            datetime(2026, 7, 8, 1, 2, 3, tzinfo=UndefinedOffset()),
        ],
        ids=["missing-timezone", "undefined-offset"],
    )
    def test_rejects_ambiguous_creation_time(
        self, created_at: datetime
    ) -> None:
        with pytest.raises(ValueError, match=r"created_at.*timezone-aware"):
            ScreenError(
                "synthetic failure", b"synthetic-image", created_at=created_at
            )

    def test_uses_utc_filename_for_offset_creation_time(
        self, tmp_path: Path
    ) -> None:
        error = ScreenError(
            "synthetic failure",
            b"synthetic-image",
            created_at=datetime(
                2026,
                7,
                8,
                1,
                2,
                3,
                tzinfo=timezone(timedelta(hours=9)),
            ),
        )

        saved_path = error.save_screenshot(tmp_path)

        assert saved_path == tmp_path / "20260707T160203Z-ScreenError.png"
        assert saved_path.read_bytes() == b"synthetic-image"

    def test_default_creation_time_uses_utc_clock(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        monkeypatch.setattr(
            screen_errors,
            "utc_now",
            lambda: datetime(2026, 7, 8, 1, 2, 3, tzinfo=UTC),
        )
        error = ScreenError("synthetic failure", b"synthetic-image")

        saved_path = error.save_screenshot(tmp_path)

        assert saved_path.name == "20260708T010203Z-ScreenError.png"


def test_screen_error_only_saves_screenshot_explicitly(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    screenshot = b"synthetic-private-image"

    def unexpected_write(*_args: object, **_kwargs: object) -> None:
        pytest.fail("Screenshot must only be written by an explicit save.")

    with monkeypatch.context() as patch:
        patch.setattr(Path, "write_bytes", unexpected_write)
        error = ScreenError("synthetic failure", screenshot)
        assert "synthetic-private-image" not in str(error)
        assert "synthetic-private-image" not in repr(error)

    assert error.screenshot is screenshot
    assert error.args == ("synthetic failure",)
    assert list(tmp_path.iterdir()) == []

    saved_path = error.save_screenshot(tmp_path)

    assert "synthetic-private-image" not in saved_path.name
    assert saved_path.read_bytes() == screenshot


@pytest.mark.parametrize("operation", ["mkdir", "write_bytes"])
def test_screen_error_propagates_screenshot_save_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    operation: str,
) -> None:
    failure = OSError("synthetic storage failure")
    error = ScreenError("synthetic failure", b"synthetic-image")

    def fail(*_args: object, **_kwargs: object) -> None:
        raise failure

    monkeypatch.setattr(Path, operation, fail)

    with pytest.raises(OSError, match="synthetic storage failure") as caught:
        error.save_screenshot(tmp_path / "failure.png")

    assert caught.value is failure
    assert list(tmp_path.iterdir()) == []


def test_inconsistent_message_error_is_screen_error() -> None:
    error = ScreenInconsistentMessageError(
        "synthetic inconsistency", b"synthetic-image"
    )

    assert isinstance(error, ScreenError)


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


def test_unimplemented_screen_operation_is_not_implemented_error() -> None:
    error = ScreenNotImplementedOperationError(
        "screen operation is not implemented",
        b"png-bytes",
    )

    assert str(error) == "screen operation is not implemented"
    assert error.screenshot == b"png-bytes"
    assert isinstance(error, ScreenError)
    assert isinstance(error, NotImplementedError)


def test_screen_unexpected_state_error_is_screen_error() -> None:
    error = ScreenUnexpectedStateError(
        "unexpected screen state",
        b"png-bytes",
    )

    assert str(error) == "unexpected screen state"
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
