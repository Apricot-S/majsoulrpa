import datetime
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from pathlib import Path
from typing import Optional

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa.common import TimeoutType


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


class Presentation(Enum):
    LOGIN = auto()
    AUTH = auto()
    HOME = auto()
    TOURNAMENT = auto()
    ROOM_BASE = auto()
    ROOM_HOST = auto()
    ROOM_GUEST = auto()
    MATCH = auto()


class PresentationCreatorBase(metaclass=ABCMeta):
    @staticmethod
    @abstractmethod
    def wait(
        browser: BrowserBase,
        timeout: TimeoutType,
        presentation: Presentation,
    ) -> None:
        pass

    @abstractmethod
    def create_new_presentation(
        self,
        current_presentation: Presentation,
        next_presentation: Presentation,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        **kwargs,
    ) -> "PresentationBase":
        pass


class PresentationBase(metaclass=ABCMeta):
    """Provides common functionality for all presentations."""

    def __init__(
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
    ) -> None:
        """Creates an instance of `PresentationBase`.

        This constructor is intended to be called only within the
        framework. Users should not directly call this constructor.

        Args:
            browser: The browser instance that is currently displaying a
                presentation.
            message_queue_client: A message queue client that is
                currently connected to the queue where mitmproxy is
                pushing messages.
            creator: A presentation creator responsible for
                instantiating presentations.
        """
        self._browser = browser
        self._message_queue_client = message_queue_client
        self._creator: PresentationCreatorBase = creator
        self._new_presentation: "PresentationBase | None" = None

    def _set_new_presentation(
        self,
        new_presentation: "PresentationBase",
    ) -> None:
        if self._new_presentation is not None:
            msg = "A new presentation has been already set."
            raise RuntimeError(msg)
        self._new_presentation = new_presentation

    def _assert_not_stale(self) -> None:
        if self._new_presentation is not None:
            msg = "The presentation has been already stale."
            raise AssertionError(msg)

    @staticmethod
    @abstractmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType) -> None:
        pass

    @property
    def new_presentation(self) -> Optional["PresentationBase"]:
        """Retrieves the new presentation.

        Returns:
            The newly transitioned-to presentation if the screen
            referred to by `self` has already transitioned; otherwise,
            `None`.
        """
        return self._new_presentation
