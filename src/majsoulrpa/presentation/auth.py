import datetime
import re
import time
from typing import Final

from majsoulrpa import RPA
from majsoulrpa._impl.browser import BrowserBase
from majsoulrpa._impl.template import Template
from majsoulrpa.common import TimeoutType, timeout_to_deadline

from .exceptions import (
    InvalidOperationError,
    PresentationNotDetectedError,
    PresentationTimeoutError,
)
from .presentation_base import (
    Presentation,
    PresentationBase,
    PresentationCreatorBase,
)

_MAX_EMAIL_ADDRESS_LENGTH: Final[int] = 50  # JP ver


class AuthPresentation(PresentationBase):
    """Authentication presentation.

    The `AuthPresentation` represents a dialog box that appears after
    the "Login" button is clicked in the `LoginPresentation`. It
    features two text boxes for entering an email address and a
    verification code, respectively. Users can perform the following
    operations with an instance of `AuthPresentation`:

    * Enter an email address in the first text box and click the "Send
      Code" button.
    * Enter a verification code in the second text box and click the
      "Login" button.
    """

    def __init__(self, rpa: RPA, creator: PresentationCreatorBase) -> None:
        """Creates an instance of `AuthPresentation`.

        This constructor is intended to be called only within the
        framework. Users should not directly call this constructor.

        Args:
            rpa: A RPA client for Mahjong Soul.
            creator: A presentation creator responsible for
                instantiating presentations.

        Raises:
            PresentationNotDetectedError: If the authentication screen
                is not detected.
        """
        super().__init__(rpa, creator)

        self._entered_email_address: bool = False
        self._last_request_time: datetime.datetime | None = None

        template = Template.open_file(
            "template/auth/marker",
            self._browser.zoom_ratio,
        )
        ss = self._browser.get_screenshot()
        if not template.match(ss):
            msg = "Could not detect `AuthPresentation`."
            raise PresentationNotDetectedError(msg, ss)

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
        """Enters an email address and clicks the "Send Code" button.

        Args:
            email_address: The email address to enter.
            timeout: The maximum duration, in seconds, to wait for the
                "Confirm" button to appear after entering the email
                address. Defaults to `10.0`.

        Raises:
            ValueError: If the email address is either unavailable or
                invalid.
            InvalidOperationError: If a request to send the verification
                code is made within 60 seconds of the previous request.
            PresentationTimeoutError: If the "Confirm" button does not
                appear within the specified timeout period.
        """
        self._assert_not_stale()

        if self._last_request_time is not None and (
            datetime.datetime.now(datetime.UTC) - self._last_request_time
            <= datetime.timedelta(seconds=60)
        ):
            msg = "Request is too frequent."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

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
        self._last_request_time = datetime.datetime.now(datetime.UTC)

    def enter_auth_code(
        self,
        auth_code: str,
        timeout: TimeoutType = 120.0,
    ) -> None:
        """Enters a verification code and clicks the "Login" button.

        Initiates a transition to the `HomePresentation` by entering a
        verification code and clicking the "Login" button, and waits
        for the home screen to appear.

        Note:
            The process to rejoin an interrupted game is not
            implemented.

        Args:
            auth_code: The verification code to enter.
            timeout: The maximum duration, in seconds, to wait for the
                home screen to appear after entering the code. Defaults
                to `120.0`.

        Raises:
            InvalidOperationError: If the email address has not been
                entered prior to this operation.
            ValueError: If the verification code is invalid or
                incorrect.
            PresentationTimeoutError: If the home screen does not
                appear within the specified timeout period.
        """
        self._assert_not_stale()

        deadline = timeout_to_deadline(timeout)

        if not self._entered_email_address:
            msg = "Email address has not been entered yet."
            raise InvalidOperationError(msg, self._browser.get_screenshot())

        # Validate the format of verification code.
        if re.fullmatch(r"\d{6}", auth_code) is None:
            msg = "Verification code must be a 6-digit number."
            raise ValueError(msg)

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

        # Check if the verification code is incorrect.
        try:
            # If the verification code is incorrect,
            # a dialog box will appear, so click "Confirm".
            template = Template.open_file(
                "template/auth/confirm",
                self._browser.zoom_ratio,
            )
            template.wait_for_then_click(self._browser, 1.0)
        except PresentationTimeoutError:
            pass
        else:
            # After clicking "Confirm",
            # it will be returned to the login screen,
            # so proceed to the authentication screen again.
            time.sleep(0.3)
            template = Template.open_file(
                "template/login/marker",
                self._browser.zoom_ratio,
            )
            template.click(self._browser)
            time.sleep(0.4)

            msg = (
                "Verification failed. Verification code may be incorrect. "
                "Please re-enter the verification code."
            )
            raise ValueError(msg)

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
                raise PresentationTimeoutError(
                    msg,
                    self._browser.get_screenshot(),
                )
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
                    self._rpa,
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
            self._rpa,
            timeout=60.0,
        )
        self._set_new_presentation(new_presentation)
