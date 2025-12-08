import asyncio
from datetime import UTC, datetime, timedelta
from typing import Self, override

from majsoulrpa import browser
from majsoulrpa.browser.driver import Key
from majsoulrpa.presentation import exceptions
from majsoulrpa.presentation.base import Presentation, require_active
from majsoulrpa.presentation.regions.login import (
    EMAIL_ADDRESS_FIELD,
    SEND_CODE,
)
from majsoulrpa.presentation.templates.login import (
    CONFIRM,
    LOGIN_1,
    UNAVAILABLE,
)

MAX_EMAIL_ADDRESS_LENGTH = 50  # JP version


class LoginPresentation(Presentation):
    @override
    def __init__(self, driver: browser.DriverBase) -> None:
        super().__init__(driver)
        self._entered_email_address = False
        self._last_request_time: datetime | None = None

    @override
    @classmethod
    async def _detect(cls, driver: browser.DriverBase) -> Self | None:
        p = cls(driver)
        await p._init_resolution()
        has_match = await p._has_match(LOGIN_1)
        return p if has_match else None

    @override
    async def _pre_dispatch(self) -> None:
        # Clicking the "Login" button ensures the email input field
        # appears. If it is already visible, the click has no effect but
        # causes no issues, so we always perform the click for
        # simplicity.
        if not await self._click_if_match(LOGIN_1):
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
            if delta <= timedelta(seconds=60):
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
        if await self._has_match(UNAVAILABLE):
            msg = "This email address is unavailable."
            ss = await self.get_screenshot()
            raise exceptions.InvalidArgumentError(msg, ss)

        # Wait for the "Confirm" button to appear, then click it.
        await asyncio.sleep(1.0)
        if not await self._click_if_match(CONFIRM):
            msg = '"Confirm" button could not be detected.'
            ss = await self.get_screenshot()
            raise exceptions.PresentationNotDetectedError(msg, ss)
        await asyncio.sleep(0.5)

        self._entered_email_address = True
        self._last_request_time = datetime.now(UTC)
