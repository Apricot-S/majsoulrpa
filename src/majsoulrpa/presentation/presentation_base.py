import datetime
from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from pathlib import Path
from typing import Optional

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa.common import TimeoutType


class BaseError(Exception):
    def __init__(self, message: str, screenshot: bytes | None) -> None:
        now = datetime.datetime.now(datetime.UTC)
        ss_name = now.strftime(f"%Y-%m-%d-%H-%M-%S-{self.__class__.__name__}")

        super().__init__(message, ss_name)
        self._screenshot = screenshot
        self._ss_name = ss_name

    def save_screenshot(self) -> None:
        if self._screenshot is not None:
            with Path(self._ss_name).with_suffix(".png").open("wb") as fp:
                fp.write(self._screenshot)


class PresentationTimeoutError(BaseError):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class PresentationNotDetectedError(BaseError):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class InconsistentMessageError(BaseError):
    def __init__(self, message: str, screenshot: bytes | None = None) -> None:
        super().__init__(message, screenshot)


class InvalidOperationError(BaseError):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class UnexpectedStateError(BaseError):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class NotImplementedOperationError(BaseError):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class BrowserRefreshRequest(BaseError):  # noqa: N818
    def __init__(
        self,
        message: str,
        browser: BrowserBase,
        screenshot: bytes | None = None,
    ) -> None:
        super().__init__(message, screenshot)
        self._browser = browser

    def refresh_browser(self) -> None:
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
    def __init__(
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
    ) -> None:
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
        return self._new_presentation
