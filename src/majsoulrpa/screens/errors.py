from datetime import UTC, datetime
from pathlib import Path

from majsoulrpa._clock import utc_now


class ScreenError(RuntimeError):
    def __init__(
        self,
        message: str,
        screenshot: bytes,
        *,
        created_at: datetime | None = None,
    ) -> None:
        super().__init__(message)
        self._screenshot = screenshot
        if created_at is None:
            created_at = utc_now()
        if created_at.utcoffset() is None:
            msg = (
                "created_at must be timezone-aware with a defined UTC offset."
            )
            raise ValueError(msg)
        self._created_at = created_at.astimezone(UTC)

    @property
    def screenshot(self) -> bytes:
        return self._screenshot

    def save_screenshot(self, path: Path) -> Path:
        screenshot_path = self._resolve_screenshot_path(path)
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        screenshot_path.write_bytes(self._screenshot)
        return screenshot_path

    def _resolve_screenshot_path(self, path: Path) -> Path:
        if path.is_dir() or path.suffix == "":
            timestamp = self._created_at.strftime("%Y%m%dT%H%M%SZ")
            return path / f"{timestamp}-{type(self).__name__}.png"
        return path


class ScreenDetectionError(ScreenError):
    pass


class ScreenDetectionTimeoutError(ScreenError, TimeoutError):
    pass


class ScreenInvalidArgumentError(ScreenError, ValueError):
    pass


class ScreenInconsistentMessageError(ScreenError):
    pass


class ScreenInvalidOperationError(ScreenError):
    pass


class ScreenNotImplementedOperationError(ScreenError, NotImplementedError):
    pass


class ScreenUnexpectedStateError(ScreenError):
    pass


class ScreenStaleError(ScreenInvalidOperationError):
    pass
