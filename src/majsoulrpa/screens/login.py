import asyncio
import re
from time import monotonic
from typing import override

from pydantic import EmailStr, TypeAdapter, ValidationError

from majsoulrpa.assets.templates.login import (
    LOGIN_1_SETTINGS_PATH,
    LOGIN_1_TEMPLATE_PATH,
    YOSTAR_LOGO_SETTINGS_PATH,
    YOSTAR_LOGO_TEMPLATE_PATH,
)
from majsoulrpa.browser.messages import YostarAuthRejectedResponse
from majsoulrpa.presentation.region import Region
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import (
    Screen,
    ScreenContext,
    ScreenDetectionSpec,
    _requires_active,
)
from majsoulrpa.screens.errors import (
    ScreenInvalidArgumentError,
    ScreenInvalidOperationError,
)

EMAIL_ADDRESS_PATTERN = re.compile(
    "[\\w!#$%&'*+/=?^_`{|}~-]+(?:\\.[\\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\\w](?:[\\w-]*[\\w])?\\.)+[\\w](?:[\\w-]*[\\w])?",
    re.ASCII,
)
"""Mahjong Soul frontend validation regex.

Some RFC-valid email addresses are rejected by this frontend validation.
"""

EMAIL_ADDRESS_ADAPTER = TypeAdapter(EmailStr)
EMAIL_ADDRESS_REENTRY_INTERVAL_SECONDS = 60.0
VERIFICATION_CODE_PATTERN = re.compile(r"[0-9]{6}", re.ASCII)


class LoginScreen(Screen):
    EMAIL_ADDRESS_REGION = Region(left=770, top=430, width=138, height=20)
    SEND_REGION = Region(left=1102, top=508, width=40, height=22)
    VERIFICATION_CODE_REGION = Region(left=768, top=508, width=100, height=20)
    LOGIN_2_REGION = Region(left=900, top=576, width=120, height=40)
    AGREEMENT_CHECKBOX_1_REGION = Region(
        left=685,
        top=467,
        width=18,
        height=18,
    )
    AGREEMENT_CHECKBOX_2_REGION = Region(
        left=685,
        top=511,
        width=18,
        height=18,
    )
    AGREEMENT_BUTTON_REGION = Region(
        left=990,
        top=713,
        width=77,
        height=30,
    )

    LOGIN_1_TEMPLATE = load_png_template_matcher(
        template_path=LOGIN_1_TEMPLATE_PATH,
        settings_path=LOGIN_1_SETTINGS_PATH,
    )
    YOSTAR_LOGO_TEMPLATE = load_png_template_matcher(
        template_path=YOSTAR_LOGO_TEMPLATE_PATH,
        settings_path=YOSTAR_LOGO_SETTINGS_PATH,
    )

    def __init__(self, context: ScreenContext | None = None) -> None:
        super().__init__(context=context)
        self._email_address_entered_at: float | None = None

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=cls.LOGIN_1_TEMPLATE.matches)

    @override
    async def before_callback(self) -> None:
        await self.click_template(
            self.LOGIN_1_TEMPLATE,
            message="Failed to find login button.",
        )

        await asyncio.sleep(1.0)

        await self.require_template(
            self.YOSTAR_LOGO_TEMPLATE,
            message="Failed to find Yostar logo after login button click.",
        )

        await asyncio.sleep(0.5)

    @_requires_active
    async def enter_email_address(self, email_address: str) -> None:
        if (
            self._email_address_entered_at is not None
            and monotonic() - self._email_address_entered_at
            < EMAIL_ADDRESS_REENTRY_INTERVAL_SECONDS
        ):
            msg = "Email address has already been entered."
            screenshot = await self.screenshot()
            raise ScreenInvalidOperationError(msg, screenshot)

        if not email_address:
            msg = "Email address cannot be empty."
            screenshot = await self.screenshot()
            raise ScreenInvalidArgumentError(msg, screenshot)

        if EMAIL_ADDRESS_PATTERN.fullmatch(email_address) is None:
            msg = "Email address is not available for Yostar login."
            screenshot = await self.screenshot()
            raise ScreenInvalidArgumentError(msg, screenshot)

        try:
            EMAIL_ADDRESS_ADAPTER.validate_python(email_address)
        except ValidationError:
            msg = "Email address is invalid."
            screenshot = await self.screenshot()
            raise ScreenInvalidArgumentError(msg, screenshot) from None

        await self.fill_region(
            self.EMAIL_ADDRESS_REGION,
            email_address,
            clear=True,
        )
        await asyncio.sleep(0.5)
        await self.click_region(self.SEND_REGION)
        self._email_address_entered_at = monotonic()
        await asyncio.sleep(3.0)

    @_requires_active
    async def enter_verification_code(self, verification_code: str) -> None:
        if self._email_address_entered_at is None:
            msg = "Email address must be entered before verification code."
            screenshot = await self.screenshot()
            raise ScreenInvalidOperationError(msg, screenshot)

        if VERIFICATION_CODE_PATTERN.fullmatch(verification_code) is None:
            msg = "Verification code must be 6 ASCII digits."
            screenshot = await self.screenshot()
            raise ScreenInvalidArgumentError(msg, screenshot)

        await self.fill_region(
            self.VERIFICATION_CODE_REGION,
            verification_code,
            clear=True,
        )
        await asyncio.sleep(0.5)
        response = await self._click_login_2_and_wait_for_yostar_auth()
        if isinstance(response, YostarAuthRejectedResponse):
            msg = "Verification code was rejected."
            screenshot = await self.screenshot()
            raise ScreenInvalidArgumentError(msg, screenshot)

        await asyncio.sleep(5.0)
        await self.click_region(self.AGREEMENT_CHECKBOX_1_REGION)
        await asyncio.sleep(0.5)
        await self.click_region(self.AGREEMENT_CHECKBOX_2_REGION)
        await asyncio.sleep(1.0)
        await self.click_region(self.AGREEMENT_BUTTON_REGION)
        self._mark_stale()

    async def _click_login_2_and_wait_for_yostar_auth(self) -> object:
        region = self.context.scale_region(self.LOGIN_2_REGION)
        x, y = region.random_point(rng=self.context.rng)
        return await self.context.browser.click_and_wait_for_yostar_auth(x, y)
