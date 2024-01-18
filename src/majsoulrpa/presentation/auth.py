import datetime
import time
from typing import Final

from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.message_queue_client import MessageQueueClientBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline

from .presentation_base import (
    InvalidOperation,
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
    PresentationNotDetected,
    Timeout,
)

_MAX_EMAIL_ADDRESS_LENGTH: Final[int] = 50  # JP ver


class AuthPresentation(PresentationBase):
    def __init__(
        self,
        browser: BrowserBase,
        message_queue_client: MessageQueueClientBase,
        creator: PresentationCreatorBase,
    ) -> None:
        super().__init__(browser, message_queue_client, creator)

        self._entered_email_address: bool = False

        template = Template.open_file(
            "template/auth/marker",
            browser.zoom_ratio,
        )
        ss = browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `AuthPresentation`."
            raise PresentationNotDetected(msg, ss)

    @staticmethod
    def _wait(browser: BrowserBase, timeout: TimeoutType = 10.0) -> None:
        template = Template.open_file(
            "template/auth/marker",
            browser.zoom_ratio,
        )
        template.wait_for(browser, timeout)

    def enter_email_address(
        self,
        email_address: str,
        timeout: TimeoutType = 10.0,
    ) -> None:
        self._assert_not_stale()

        if len(email_address) > _MAX_EMAIL_ADDRESS_LENGTH:
            msg = (
                "Keep your email address "
                f"within {_MAX_EMAIL_ADDRESS_LENGTH} characters."
            )
            raise ValueError(msg)

        # Click the "Enter email address" text box to focus it.
        self._browser.click_region(
            int(365 * self._browser.zoom_ratio),
            int(385 * self._browser.zoom_ratio),
            int(200 * self._browser.zoom_ratio),
            int(30 * self._browser.zoom_ratio),
        )
        time.sleep(0.1)

        # Enter an email address in the text box.
        self._browser.press_hotkey("Control", "KeyA")
        self._browser.press("Backspace")
        self._browser.write(email_address)

        # Click the "Send Code" button.
        self._browser.click_region(
            int(850 * self._browser.zoom_ratio),
            int(500 * self._browser.zoom_ratio),
            int(190 * self._browser.zoom_ratio),
            int(70 * self._browser.zoom_ratio),
        )

        # Check if the email address is unavailable.
        template = Template.open_file(
            "template/auth/unavailable",
            self._browser.zoom_ratio,
        )
        if template.match(self._browser.get_screenshot()):
            msg = "This email address is unavailable."
            raise ValueError(msg)

        # Wait for the "Confirm" button to appear, then click it.
        template = Template.open_file(
            "template/auth/confirm",
            self._browser.zoom_ratio,
        )
        template.wait_for_then_click(self._browser, timeout)
        time.sleep(0.1)

        self._entered_email_address = True

    def enter_auth_code(
        self,
        auth_code: str,
        timeout: TimeoutType = 120.0,
    ) -> None:
        self._assert_not_stale()

        if self._entered_email_address is False:
            msg = "Email address has not been entered yet."
            raise InvalidOperation(msg, self._browser.get_screenshot())

        deadline = timeout_to_deadline(timeout)

        # Click the "Enter the verification code sent to your email"
        # text box to focus it.
        self._browser.click_region(
            int(365 * self._browser.zoom_ratio),
            int(520 * self._browser.zoom_ratio),
            int(140 * self._browser.zoom_ratio),
            int(35 * self._browser.zoom_ratio),
        )
        time.sleep(0.1)

        # Enter an auth code in the text box.
        self._browser.press_hotkey("Control", "KeyA")
        self._browser.press("Backspace")
        self._browser.write(auth_code)

        # Wait for the "Login" button to appear, then click it.
        template = Template.open_file(
            "template/auth/login",
            self._browser.zoom_ratio,
        )
        template.wait_for_then_click(self._browser, timeout)

        paths = (
            "template/home/marker0",
            "template/match/marker0",
            "template/match/marker1",
            "template/match/marker2",
            "template/match/marker3",
        )
        templates = [
            Template.open_file(p, self._browser.zoom_ratio) for p in paths
        ]

        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout."
                raise Timeout(msg, self._browser.get_screenshot())
            index = Template.match_one_of(
                self._browser.get_screenshot(),
                templates,
            )
            if index in (0,):
                break
            if index in (1, 2, 3, 4):
                # TODO: What to do when a suspended match is resumed.
                timeout = deadline - datetime.datetime.now(datetime.UTC)
                self._creator.wait(self._browser, timeout, Presentation.MATCH)
                timeout = deadline - datetime.datetime.now(datetime.UTC)
                new_presentation = self._creator.create_new_presentation(
                    Presentation.AUTH,
                    Presentation.MATCH,
                    self._browser,
                    self._message_queue_client,
                    timeout=timeout,
                )
                self._set_new_presentation(new_presentation)
                return

        # Wait until the home screen is displayed.
        timeout = deadline - datetime.datetime.now(datetime.UTC)
        self._creator.wait(self._browser, timeout, Presentation.HOME)

        new_presentation = self._creator.create_new_presentation(
            Presentation.AUTH,
            Presentation.HOME,
            self._browser,
            self._message_queue_client,
            timeout=60.0,
        )
        self._set_new_presentation(new_presentation)
