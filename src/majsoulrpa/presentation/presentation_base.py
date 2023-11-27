from typing import Optional

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase


class ErrorBase(Exception):  # noqa: N818
    def __init__(self, message: str, screenshot: bytes | None) -> None:
        self._message = message
        self._screenshot = screenshot


class Timeout(ErrorBase):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class PresentationNotDetected(ErrorBase):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class StalePresentation(ErrorBase):
    def __init__(self, message: str, screenshot: bytes) -> None:
        super().__init__(message, screenshot)


class PresentationNotUpdated(ErrorBase):
    def __init__(self, message: str, screenshot: bytes | None) -> None:
        super().__init__(message, screenshot)


class InconsistentMessage(ErrorBase):
    def __init__(self, message: str, screenshot: bytes | None = None) -> None:
        super().__init__(message, screenshot)


class InvalidOperation(ErrorBase):
        def __init__(self, message: str, screenshot: bytes) -> None:
            super().__init__(message, screenshot)


class BrowserRefreshRequest(ErrorBase):
    def __init__(
        self, message: str,
        browser: BrowserBase,
        screenshot: bytes | None = None,
    ) -> None:
        super().__init__(message, screenshot)
        self._browser = browser

    def refresh_browser(self) -> None:
        self._browser.refresh()


class PresentationBase:

    def __init__(self, browser: BrowserBase, db_client: DBClientBase) -> None:
        self._browser = browser
        self._db_client = db_client
        self._new_presentation: "PresentationBase" | None = None

    def _set_new_presentation(self,
                              new_presentation: "PresentationBase") -> None:
        if self._new_presentation is not None:
            msg = "A new presentation has been already set."
            raise RuntimeError(msg)
        self._new_presentation = new_presentation

    def _assert_not_stale(self) -> None:
        if self._new_presentation is not None:
            msg = "The presentation has been already stale."
            raise AssertionError(msg)

    @property
    def new_presentation(self) -> Optional["PresentationBase"]:
        return self._new_presentation
