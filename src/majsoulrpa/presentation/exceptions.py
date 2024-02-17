"""Provides exception classes that is thrown from presentation."""

import datetime
from pathlib import Path

from majsoulrpa._impl.browser import BrowserBase


class BaseError(Exception):
    """A basic error.

    A basic error occurring in this framework. It can record a
    screenshot where the error occurred.
    """

    def __init__(self, message: str, screenshot: bytes | None) -> None:
        """Creates an instance of `BaseError`.

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

    def save_screenshot(self) -> None:
        """Saves the screenshot to a file."""
        if self._screenshot is not None:
            with Path(self._ss_name).with_suffix(".png").open("wb") as fp:
                fp.write(self._screenshot)


class PresentationTimeoutError(BaseError):
    """A timeout error.

    Occurs when a presentation is not detected within the specified
    timeout period.
    """

    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class PresentationNotDetectedError(BaseError):
    """A presentation not detected error.

    Occurs when the expected presentation fails to be detected.
    """

    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class InconsistentMessageError(BaseError):
    """An inconsistent message error.

    Occurs when messages exchanged between the browser and the Mahjong
    Soul server do not match the expected sequence or type.
    """

    def __init__(self, message: str, screenshot: bytes | None = None) -> None:
        super().__init__(message, screenshot)


class InvalidOperationError(BaseError):
    """An invalid operation error.

    Occurs when an operation is attempted that is invalid given the
    current state of the presentation.
    """

    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class UnexpectedStateError(BaseError):
    """An unexpected state error.

    Occurs when the presentation enters an unexpected state.
    """

    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class NotImplementedOperationError(BaseError):
    """Not implemented operation Error.

    Occurs when an operation is not implemented.
    """

    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class BrowserRefreshRequest(BaseError):  # noqa: N818
    """A browser refresh request.

    Indicates an error that might be resolved by reloading the web page.
    This error should be caught and handled at the appropriate point in
    the code, with an attempt to resume operations through page reload.
    """

    def __init__(
        self,
        message: str,
        browser: BrowserBase,
        screenshot: bytes | None = None,
    ) -> None:
        """Creates an instance of `BrowserRefreshRequest`.

        Args:
            message: A message describing the error.
            browser: The browser instance handling the display when the
                error occurred.
            screenshot: A screenshot encoded in PNG format captured at
                the point where the error occurred, if any. Defaults to
                `None`.
        """
        super().__init__(message, screenshot)
        self._browser = browser

    def refresh_browser(self) -> None:
        """Refresh the browser."""
        self._browser.refresh()
