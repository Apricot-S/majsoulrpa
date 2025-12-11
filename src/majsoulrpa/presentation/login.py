import asyncio
import re
from datetime import UTC, datetime, timedelta
from typing import ClassVar, Self, override

from majsoulrpa import browser, sniffer
from majsoulrpa.browser.driver import Key
from majsoulrpa.presentation import exceptions
from majsoulrpa.presentation.base import Presentation, require_active
from majsoulrpa.presentation.regions.login import (
    EMAIL_ADDRESS_FIELD,
    SEND_CODE,
    VERIFICATION_CODE_FIELD,
)
from majsoulrpa.presentation.templates.login import (
    CONFIRM,
    LOGIN_1,
    LOGIN_2,
    UNAVAILABLE,
)

MAX_EMAIL_ADDRESS_LENGTH = 50  # JP version
REQUEST_INTERVAL = timedelta(seconds=60)
VERIFICATION_CODE_PATTERN = re.compile(r"\d{6}")


class LoginPresentation(Presentation):
    _templates: ClassVar = {
        "confirm": CONFIRM,
        "login_1": LOGIN_1,
        "login_2": LOGIN_2,
        "unavailable": UNAVAILABLE,
    }

    @override
    def __init__(
        self,
        driver: browser.DriverBase,
        message_queue: sniffer.MessageQueueBase,
    ) -> None:
        super().__init__(driver, message_queue)
        self._entered_email_address = False
        self._last_request_time: datetime | None = None

    @override
    @classmethod
    async def _detect(
        cls,
        driver: browser.DriverBase,
        message_queue: sniffer.MessageQueueBase,
    ) -> Self | None:
        p = cls(driver, message_queue)
        await p._init_resolution()
        has_match = await p._has_match(cls._templates["login_1"])
        return p if has_match else None

    @override
    async def _pre_dispatch(self) -> None:
        # Clicking the "Login" button ensures the email input field
        # appears. If it is already visible, the click has no effect but
        # causes no issues, so we always perform the click for
        # simplicity.
        if not await self._click_if_match(self._templates["login_1"]):
            msg = '"Login" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)
        await asyncio.sleep(0.5)

    @require_active
    async def enter_email_address(self, email_address: str) -> None:
        if len(email_address) > MAX_EMAIL_ADDRESS_LENGTH:
            msg = f"Keep an email address within {MAX_EMAIL_ADDRESS_LENGTH} characters."  # noqa: E501
            raise exceptions.InvalidArgumentError(msg, None)

        if self._last_request_time is not None:
            delta = datetime.now(UTC) - self._last_request_time
            if delta <= REQUEST_INTERVAL:
                msg = "Request is too frequent."
                ss = await self.get_screenshot()
                raise exceptions.InvalidOperationError(msg, ss)

        # Click the "Enter email address" text box to focus it.
        await self._click_region(EMAIL_ADDRESS_FIELD)
        await asyncio.sleep(0.5)

        # Select all existing text in the email address field.
        await self._press_key([Key.CONTROL_OR_META, "a"])
        await asyncio.sleep(0.5)

        # Clear the selected text.
        await self._press_key(Key.BACKSPACE)
        await asyncio.sleep(0.5)

        # Enter an email address in the text box.
        await self._type_key(email_address)
        await asyncio.sleep(0.5)

        # Click the "Send Code" button.
        await self._click_region(SEND_CODE)
        await asyncio.sleep(0.2)

        # Check if the email address is unavailable.
        if await self._has_match(self._templates["unavailable"]):
            msg = "This email address is unavailable."
            ss = await self.get_screenshot()
            raise exceptions.InvalidArgumentError(msg, ss)

        # Wait for the "Confirm" button to appear, then click it.
        await asyncio.sleep(1.0)
        if not await self._click_if_match(self._templates["confirm"]):
            msg = '"Confirm" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)
        await asyncio.sleep(0.5)

        self._entered_email_address = True
        self._last_request_time = datetime.now(UTC)

    @require_active
    async def enter_verification_code(self, verification_code: str) -> None:
        # Validate the format of verification code.
        if VERIFICATION_CODE_PATTERN.fullmatch(verification_code) is None:
            msg = "Verification code must be a 6-digit number."
            raise exceptions.InvalidArgumentError(msg, None)

        if not self._entered_email_address:
            msg = "Email address has not been entered yet."
            raise exceptions.InvalidOperationError(msg, None)

        # Click the "Enter the verification code sent to your email"
        # text box to focus it.
        await self._click_region(VERIFICATION_CODE_FIELD)
        await asyncio.sleep(0.5)

        # Select all existing text in the email address field.
        await self._press_key([Key.CONTROL_OR_META, "a"])
        await asyncio.sleep(0.5)

        # Clear the selected text.
        await self._press_key(Key.BACKSPACE)
        await asyncio.sleep(0.5)

        # Enter the verification code in the text box.
        await self._type_key(verification_code)
        await asyncio.sleep(0.5)

        # Click the enabled "Login" button.
        if not await self._click_if_match(self._templates["login_2"]):
            msg = '"Login" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)

        # Check if the verification code is incorrect.
        # If the verification code is incorrect,
        # a dialog box will appear, so click "Confirm".
        await asyncio.sleep(1.5)
        if await self._click_if_match(self._templates["confirm"]):
            # After clicking "Confirm", the email input field closes,
            # so click the "Login" button to reopen it.
            await asyncio.sleep(1.0)
            if not await self._click_if_match(self._templates["login_1"]):
                msg = '"Login" button could not be detected.'
                ss = await self.get_screenshot()
                raise exceptions.PresentationNotDetectedError(msg, ss)
            await asyncio.sleep(0.5)

            msg = "Verification failed. Verification code may be incorrect."
            raise exceptions.InvalidArgumentError(msg, None)

        self._mark_finished()
