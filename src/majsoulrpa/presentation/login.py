import asyncio
import re
from datetime import UTC, datetime, timedelta
from typing import ClassVar, Self, override

import majsoulrpa.presentation.regions.login as login_regions
import majsoulrpa.presentation.templates.login as login_templates
from majsoulrpa import browser, sniffer
from majsoulrpa.browser.driver import Key
from majsoulrpa.presentation import exceptions
from majsoulrpa.presentation.base import Presentation, rpa_api

REQUEST_INTERVAL = timedelta(seconds=60)
MAX_EMAIL_ADDRESS_LENGTH = 254
MAX_EMAIL_LOCAL_PART_LENGTH = 64
MAX_EMAIL_DOMAIN_LENGTH = 253
MAX_EMAIL_DOMAIN_LABEL_LENGTH = 63
EMAIL_ADDRESS_PATTERN = re.compile(
    r"[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?",
    re.ASCII,
)
DOMAIN_LABEL_PATTERN = re.compile(r"[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?")
VERIFICATION_CODE_PATTERN = re.compile(r"\d{6}")


def validate_email_address(email_address: str) -> None:
    if not email_address:
        msg = "Email address cannot be empty."
        raise exceptions.InvalidArgumentError(msg, None)

    if EMAIL_ADDRESS_PATTERN.fullmatch(email_address) is None:
        msg = "Email address is not available for Yostar login."
        raise exceptions.InvalidArgumentError(msg, None)

    local_part, domain = email_address.rsplit("@", maxsplit=1)
    if (
        len(email_address) > MAX_EMAIL_ADDRESS_LENGTH
        or len(local_part) > MAX_EMAIL_LOCAL_PART_LENGTH
        or len(domain) > MAX_EMAIL_DOMAIN_LENGTH
    ):
        msg = "Email address is invalid."
        raise exceptions.InvalidArgumentError(msg, None)

    if any(
        len(label) > MAX_EMAIL_DOMAIN_LABEL_LENGTH
        or DOMAIN_LABEL_PATTERN.fullmatch(label) is None
        for label in domain.split(".")
    ):
        msg = "Email address is invalid."
        raise exceptions.InvalidArgumentError(msg, None)


class LoginPresentation(Presentation):
    _templates: ClassVar = {
        "confirm": login_templates.CONFIRM,
        "login_1": login_templates.LOGIN_1,
        "login_2": login_templates.LOGIN_2,
        "ok": login_templates.OK,
        "send": login_templates.SEND,
    }
    _regions: ClassVar = {
        "email_address_field": login_regions.EMAIL_ADDRESS_FIELD,
        "send": login_regions.SEND,
        "verification_code_field": login_regions.VERIFICATION_CODE_FIELD,
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

    async def _detect_maintenance(self) -> None:
        if await self._has_match(self._templates["ok"]):
            msg = "Login cannot proceed during server maintenance."
            ss = await self.get_screenshot()
            raise exceptions.UnexpectedStateError(msg, ss)

    @rpa_api
    async def enter_email_address(self, email_address: str) -> None:
        await self._detect_maintenance()

        validate_email_address(email_address)

        if self._last_request_time is not None:
            delta = datetime.now(UTC) - self._last_request_time
            if delta <= REQUEST_INTERVAL:
                msg = "Request is too frequent."
                ss = await self.get_screenshot()
                raise exceptions.InvalidOperationError(msg, ss)

        # Click the "Enter email address" text box to focus it.
        await self._click_region(self._regions["email_address_field"])
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

        # Click the "Send" button.
        await self._click_region(self._regions["send"])
        await asyncio.sleep(3.0)

        # Check if the "Send" button has changed to the countdown timer
        # indicating the interval until resending becomes available.
        # If it has not changed, it remains as the "Send" button.
        if await self._has_match(self._templates["send"]):
            msg = "This email address is unavailable."
            ss = await self.get_screenshot()
            raise exceptions.InvalidArgumentError(msg, ss)

        self._entered_email_address = True
        self._last_request_time = datetime.now(UTC)

    @rpa_api
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
        await self._click_region(self._regions["verification_code_field"])
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

        await self._detect_maintenance()

        self._mark_finished()
