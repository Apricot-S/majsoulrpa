"""Errors used in presentation."""

import datetime
from pathlib import Path
from typing import override


class BaseError(Exception):
    """A basic error.

    A basic error occurring in `Presentation`. It can record a
    screenshot where the error occurred.
    """

    def __init__(self, message: str, screenshot: bytes | None) -> None:
        """Initializes the instance.

        Args:
            message: A message describing the error.
            screenshot: A screenshot encoded in PNG format captured at
                the point where the error occurred, if any.
        """
        now = datetime.datetime.now(datetime.UTC)
        ss_name = now.strftime(f"%Y-%m-%d-%H-%M-%S-{self.__class__.__name__}")

        super().__init__(message, ss_name)
        self._screenshot = screenshot
        self._ss_name = ss_name

    @property
    def screenshot(self) -> bytes | None:
        return self._screenshot

    def save_screenshot(self, directory: Path) -> None:
        """Saves the screenshot to a PNG file.

        Args:
            directory: The directory where the screenshot file will be
                saved.

        Raises:
            FileNotFoundError: If the specified directory does not
                exist.
            OSError: If writing the file fails due to I/O issues.

        Note:
            If no screenshot is available, nothing is saved.
            This method does not create the directory automatically.
        """
        if self._screenshot is not None:
            file_path = directory / Path(self._ss_name).with_suffix(".png")
            with file_path.open("wb") as fp:
                fp.write(self._screenshot)


class PresentationTimeoutError(BaseError):
    """A timeout error.

    Raised when a presentation is not detected within the specified
    timeout period.
    """

    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class PresentationNotDetectedError(BaseError):
    """A presentation not detected error.

    Raised when the expected presentation fails to be detected.
    """

    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class InvalidOperationError(BaseError):
    """An invalid operation error.

    Raised when an operation is attempted that is invalid given the
    current state of the presentation.
    """

    @override
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)
