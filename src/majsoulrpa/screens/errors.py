from datetime import UTC, datetime
from pathlib import Path


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
        self._created_at = created_at or datetime.now(UTC)

    def screenshot(self) -> bytes:
        return self._screenshot

    def save_screenshot(self, path: Path) -> Path:
        screenshot_path = self._resolve_screenshot_path(path)
        screenshot_path.parent.mkdir(parents=True, exist_ok=True)
        screenshot_path.write_bytes(self._screenshot)
        return screenshot_path

    def _resolve_screenshot_path(self, path: Path) -> Path:
        if path.is_dir() or path.suffix == "":
            timestamp = self._created_at.astimezone(UTC).strftime(
                "%Y%m%dT%H%M%SZ",
            )
            return path / f"{timestamp}-{type(self).__name__}.png"
        return path


class ScreenDetectionError(ScreenError):
    pass


class ScreenDetectionTimeoutError(ScreenError):
    pass
