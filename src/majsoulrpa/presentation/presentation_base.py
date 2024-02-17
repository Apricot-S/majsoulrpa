from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from typing import Optional

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa.common import TimeoutType


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
