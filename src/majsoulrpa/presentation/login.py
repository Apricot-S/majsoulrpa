import datetime

from majsoulrpa import RPA
from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline

from .exceptions import PresentationNotDetectedError, PresentationTimeoutError
from .presentation_base import (
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
)


class LoginPresentation(PresentationBase):
    """Login presentation.

    The `LoginPresentation` represents the first screen displayed to
    users who are not logged in when they navigate to
    https://game.mahjongsoul.com/ in their browser. Users can perform
    the following operation with an instance of `LoginPresentation`:

    * Click the "Login" button to transition to the `AuthPresentation`.
    """

    def __init__(self, rpa: RPA, creator: PresentationCreatorBase) -> None:
        """Creates an instance of `LoginPresentation`.

        This constructor is intended to be called only within the
        framework. Users should not directly call this constructor.

        Args:
            rpa: A RPA client for Mahjong Soul.
            creator: A presentation creator responsible for
                instantiating presentations.

        Raises:
            PresentationNotDetectedError: If the login screen is not
                detected.
        """
        super().__init__(rpa, creator)

        template = Template.open_file(
            "template/login/marker",
            self._browser.zoom_ratio,
        )
        ss = self._browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `LoginPresentation`."
            raise PresentationNotDetectedError(msg, ss)

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 60.0) -> None:
        template = Template.open_file(
            "template/login/marker",
            browser.zoom_ratio,
        )
        template.wait_for(browser, timeout)

    def login(self, timeout: TimeoutType = 60.0) -> None:
        """Clicks the "Login" button.

        Initiates a transition to the `AuthPresentation` by clicking the
        "Login" button, and waits for the authentication screen to
        appear.

        Args:
            timeout: The maximum duration, in seconds, to wait for the
                authentication screen to appear. Defaults to `60.0`.

        Raises:
            PresentationTimeoutError: If the authentication screen does
                not appear within the specified timeout period.
        """
        self._assert_not_stale()

        template = Template.open_file(
            "template/login/marker",
            self._browser.zoom_ratio,
        )
        template.click(self._browser)

        deadline = timeout_to_deadline(timeout)
        while True:
            now = datetime.datetime.now(datetime.UTC)
            if now > deadline:
                msg = "Timeout in transition from `login`."
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )

            new_presentation: PresentationBase | None = None
            try:
                new_presentation = self._creator.create_new_presentation(
                    Presentation.LOGIN,
                    Presentation.AUTH,
                    self._rpa,
                )
                self._set_new_presentation(new_presentation)
            except PresentationNotDetectedError:
                pass
            else:
                return

            try:
                now = datetime.datetime.now(datetime.UTC)
                new_presentation = self._creator.create_new_presentation(
                    Presentation.LOGIN,
                    Presentation.HOME,
                    self._rpa,
                    timeout=(deadline - now),
                )
                self._set_new_presentation(new_presentation)
            except PresentationNotDetectedError:
                pass
            else:
                return
