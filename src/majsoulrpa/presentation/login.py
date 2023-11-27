import datetime

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType

from .auth import AuthPresentation
from .home import HomePresentation
from .presentation_base import (
    PresentationBase,
    PresentationNotDetected,
    Timeout,
)


class LoginPresentation(PresentationBase):

    def __init__(self, browser: BrowserBase, db_client: DBClientBase) -> None:
        super().__init__(browser=browser, db_client=db_client)

        template = Template.open_file("template/login/marker",
                                      browser.zoom_ratio)
        sct = browser.get_screenshot()
        if not template.match(sct):
            msg = "Could not detect 'LoginPresentation'."
            raise PresentationNotDetected(msg, sct)

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

            p: PresentationBase | None = None
            try:
                p = AuthPresentation(self._browser, self._db_client)
                self._set_new_presentation(p)
            except PresentationNotDetected:
                pass
            else:
                return

            try:
                now = datetime.datetime.now(datetime.UTC)
                p = HomePresentation(
                    self._browser, self._db_client, deadline - now,
                )
                self._set_new_presentation(p)
            except PresentationNotDetected:
                pass
            else:
                return
