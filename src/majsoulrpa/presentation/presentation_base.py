from abc import ABCMeta, abstractmethod
from enum import Enum, auto
from typing import Optional

from majsoulrpa import RPA
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
        rpa: RPA,
        **kwargs,
    ) -> "PresentationBase":
        pass


class PresentationBase(metaclass=ABCMeta):
    """Provides common functionality for all presentations."""

    def __init__(self, rpa: RPA, creator: PresentationCreatorBase) -> None:
        """Creates an instance of `PresentationBase`.

        This constructor is intended to be called only within the
        framework. Users should not directly call this constructor.

        Args:
            rpa: A RPA client for Mahjong Soul.
            creator: A presentation creator responsible for
                instantiating presentations.
        """
        self._rpa = rpa
        self._creator: PresentationCreatorBase = creator
        self._new_presentation: PresentationBase | None = None

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
    def _browser(self) -> BrowserBase:
        if self._rpa._browser is None:  # noqa: SLF001
            msg = "Browser is not running."
            raise RuntimeError(msg)
        return self._rpa._browser  # noqa: SLF001

    @property
    def _message_queue_client(self) -> MessageQueueClientBase:
        if self._rpa._message_queue_client is None:  # noqa: SLF001
            msg = "Message queue client is not running."
            raise RuntimeError(msg)
        return self._rpa._message_queue_client  # noqa: SLF001

    @property
    def new_presentation(self) -> Optional["PresentationBase"]:
        """Retrieves the new presentation.

        Returns:
            The newly transitioned-to presentation if the screen
            referred to by `self` has already transitioned; otherwise,
            `None`.
        """
        return self._new_presentation
