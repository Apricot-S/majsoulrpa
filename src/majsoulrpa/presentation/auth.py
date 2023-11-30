import datetime
import time
from typing import Final

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.db_client import DBClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType

from .presentation_base import (
    InvalidOperation,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    PresentationNotDetected,
    Timeout,
)

_TEXT_BOX_EMAIL_ADDRESS_LEFT: Final[int] = 365
_TEXT_BOX_EMAIL_ADDRESS_TOP: Final[int] = 385
_TEXT_BOX_EMAIL_ADDRESS_WIDTH: Final[int] = 200
_TEXT_BOX_EMAIL_ADDRESS_HEIGHT: Final[int] = 30

_BUTTON_SEND_CODE_LEFT: Final[int] = 850
_BUTTON_SEND_CODE_TOP: Final[int] = 500
_BUTTON_SEND_CODE_WIDTH: Final[int] = 190
_BUTTON_SEND_CODE_HEIGHT: Final[int] = 70

_TEXT_BOX_AUTH_CODE_LEFT: Final[int] = 365
_TEXT_BOX_AUTH_CODE_TOP: Final[int] = 520
_TEXT_BOX_AUTH_CODE_WIDTH: Final[int] = 140
_TEXT_BOX_AUTH_CODE_HEIGHT: Final[int] = 35


class AuthPresentation(PresentationBase):

    def __init__(
        self, browser: BrowserBase, db_client: DBClientBase,
        creator: PresentationCreatorBase,
    ) -> None:
        super().__init__(browser, db_client, creator)

        self._entered_email_address: bool = False

        template = Template.open_file("template/auth/marker",
                                      browser.zoom_ratio)
        sct = browser.get_screenshot()
        if not template.match(sct):
            msg = "Could not detect 'AuthPresentation'."
            raise PresentationNotDetected(msg, sct)

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 10.0) -> None:
        template = Template.open_file("template/auth/marker",
                                      browser.zoom_ratio)
        template.wait_for(browser, timeout)

    def enter_email_address(
        self, email_address: str, timeout: TimeoutType = 10.0,
    ) -> None:
        self._assert_not_stale()

        if self._entered_email_address is True:
            msg = "Email address has been already entered."
            raise InvalidOperation(msg, self._browser.get_screenshot())

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        # Click the "Enter email address" text box to focus it.
        self._browser.click_region(
            int(_TEXT_BOX_EMAIL_ADDRESS_LEFT * self._browser.zoom_ratio),
            int(_TEXT_BOX_EMAIL_ADDRESS_TOP * self._browser.zoom_ratio),
            int(_TEXT_BOX_EMAIL_ADDRESS_WIDTH * self._browser.zoom_ratio),
            int(_TEXT_BOX_EMAIL_ADDRESS_HEIGHT * self._browser.zoom_ratio),
        )
        time.sleep(0.1)

        # Enter an email address in the text box.
        self._browser.press_hotkey("Control", "KeyA")
        self._browser.press("Backspace")
        self._browser.write(email_address)
        self._entered_email_address = True

        # Click the "Send Code" button.
        self._browser.click_region(
            int(_BUTTON_SEND_CODE_LEFT * self._browser.zoom_ratio),
            int(_BUTTON_SEND_CODE_TOP * self._browser.zoom_ratio),
            int(_BUTTON_SEND_CODE_WIDTH * self._browser.zoom_ratio),
            int(_BUTTON_SEND_CODE_HEIGHT * self._browser.zoom_ratio),
        )

        # Wait for the dialog box to appear.
        template = Template.open_file("template/auth/confirm",
                                      self._browser.zoom_ratio)
        template.wait_for(self._browser, timeout)

        # Click the "Confirm" button.
        template.click(self._browser)
        time.sleep(0.1)

    def enter_auth_code(
        self, auth_code: str, timeout: TimeoutType = 120.0,
    ) -> None:
        self._assert_not_stale()

        if self._entered_email_address is False:
            msg = "Email address has not been entered yet."
            raise InvalidOperation(msg, self._browser.get_screenshot())

        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout

        # Click the "Enter the verification code sent to your email"
        # text box to focus it.
        self._browser.click_region(
            int(_TEXT_BOX_AUTH_CODE_LEFT * self._browser.zoom_ratio),
            int(_TEXT_BOX_AUTH_CODE_TOP * self._browser.zoom_ratio),
            int(_TEXT_BOX_AUTH_CODE_WIDTH * self._browser.zoom_ratio),
            int(_TEXT_BOX_AUTH_CODE_HEIGHT * self._browser.zoom_ratio),
        )
        time.sleep(0.1)

        # Enter an auth code in the text box.
        self._browser.press_hotkey("Control", "KeyA")
        self._browser.press("Backspace")
        self._browser.write(auth_code)

        # Wait for the "Login" button to be activated.
        template = Template.open_file("template/auth/login",
                                      self._browser.zoom_ratio)
        template.wait_for(self._browser, timeout)

        # Click the "Login" button
        template.click(self._browser)

        templates = (
            "template/home/marker0",
        )

        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, self._browser.get_screenshot())
            index = Template.match_one_of(
                self._browser.get_screenshot(),
                templates,
                self._browser.zoom_ratio,
            )
            if index in (0,):
                break

            time.sleep(0.5)

        # Wait until the home screen is displayed.
        timeout = deadline - datetime.datetime.now(datetime.UTC)
        self._creator.wait(self._browser, timeout, Presentation.HOME)

        new_presentation = self._creator.create_new_presentation(
            Presentation.AUTH, Presentation.HOME,
            self._browser, self._db_client, timeout=60.0,
        )
        self._set_new_presentation(new_presentation)
