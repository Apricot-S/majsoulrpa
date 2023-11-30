import datetime
from typing import NoReturn

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType

from .presentation_base import (
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    PresentationNotDetected,
    Timeout,
)


class LoginPresentation(PresentationBase):

    def __init__(
        self, browser: BrowserBase, db_client: DBClientBase,
        creator: PresentationCreatorBase,
    ) -> None:
        super().__init__(browser, db_client, creator)

        template = Template.open_file("template/login/marker",
                                      browser.zoom_ratio)
        sct = browser.get_screenshot()
        if not template.match(sct):
            msg = "Could not detect 'LoginPresentation'."
            raise PresentationNotDetected(msg, sct)

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType) -> NoReturn:  # noqa: ARG004
        raise AssertionError

    def login(self, timeout: TimeoutType = 60.0) -> None:
        self._assert_not_stale()

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        template = Template.open_file("template/login/marker",
                                      self._browser.zoom_ratio)
        template.click(self._browser)

        deadline = datetime.datetime.now(datetime.UTC) + timeout
        while True:
            now = datetime.datetime.now(datetime.UTC)
            if now > deadline:
                msg = "Timeout in transition from 'login'."
                raise Timeout(msg, self._browser.get_screenshot())

            new_presentation: PresentationBase | None = None
            try:
                new_presentation = self._creator.create_new_presentation(
                    Presentation.LOGIN, Presentation.AUTH,
                    self._browser, self._db_client,
                )
                self._set_new_presentation(new_presentation)
            except PresentationNotDetected:
                pass
            else:
                return

            try:
                now = datetime.datetime.now(datetime.UTC)
                new_presentation = self._creator.create_new_presentation(
                    Presentation.LOGIN, Presentation.HOME,
                    self._browser, self._db_client, timeout=(deadline - now),
                )
                self._set_new_presentation(new_presentation)
            except PresentationNotDetected:
                pass
            else:
                return
