"""Errors used in presentation."""

import datetime
from pathlib import Path
from typing import override


class BaseError(Exception):
    """Base exception for errors raised in `Presentation`.

    Can record a screenshot at the point where the error occurred.
    """

    def __init__(self, message: str, screenshot: bytes | None) -> None:
        """Initializes the instance.

        Args:
            message: A message describing the error.
            screenshot: A screenshot encoded in PNG format captured at
                the point where the error occurred, if any.
        """
        now = datetime.datetime.now(datetime.UTC)
        self._timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
        self._screenshot = screenshot
        super().__init__(message, self._timestamp)

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
        if self._screenshot is None:
            return

        file_name = f"{self._timestamp}-{self.__class__.__name__}.png"
        file_path = directory / Path(file_name)
        with file_path.open("wb") as fp:
            fp.write(self._screenshot)


class PresentationTimeoutError(BaseError):
    """Error raised when a presentation is not detected within
    the timeout period.
    """

    @override
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class PresentationNotDetectedError(BaseError):
    """Error raised when the expected presentation cannot be
    detected.
    """

    @override
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class InvalidOperationError(BaseError):
    """Error raised when an operation is attempted
    that is invalid for the current state of the presentation.
    """


class InvalidArgumentError(BaseError):
    """Error raised when an operation is called
    with invalid arguments.
    """


class UnexpectedStateError(BaseError):
    """Error raised when the presentation enters an unexpected state."""
