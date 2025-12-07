import asyncio
from typing import Self, override

from majsoulrpa import browser
from majsoulrpa.browser.driver import Key
from majsoulrpa.presentation.base import Presentation
from majsoulrpa.presentation.delay import get_random_delay
from majsoulrpa.presentation.region import Region
from majsoulrpa.presentation.template import (
    IMAGE_PATH,
    Config,
    FileImage,
    Matcher,
)

_LOGIN_BUTTON_IMAGE = FileImage(IMAGE_PATH / "login/login_button_1.png")
_LOGIN_BUTTON_CONFIG = Config.from_file(
    IMAGE_PATH / "login/login_button_1.toml",
)
_LOGIN_BUTTON = Matcher(_LOGIN_BUTTON_IMAGE, _LOGIN_BUTTON_CONFIG)

_EMAIL_ADDRESS_FIELD = Region(365, 385, 200, 30)
_SEND_CODE_BUTTON = Region(850, 500, 190, 70)


class LoginPresentation(Presentation):
    @override
    def __init__(self, driver: browser.DriverBase) -> None:
        super().__init__(driver)

    @override
    @classmethod
    async def _detect(cls, driver: browser.DriverBase) -> Self | None:
        p = cls(driver)
        await p._init_resolution()
        has_match = await p._has_match(_LOGIN_BUTTON)
        return p if has_match else None

    @override
    async def _pre_dispatch(self) -> None:
        # Clicking the "Login" button ensures the email input field
        # appears. If it is already visible, the click has no effect but
        # causes no issues, so we always perform the click for
        # simplicity.
        await self._click_if_match(_LOGIN_BUTTON)
        # TODO: クリックできなかったときの例外を追加する
        await asyncio.sleep(0.5)

    @Presentation._require_active  # noqa: SLF001
    async def enter_email_address(self, email: str) -> None:
        # Click the "Enter email address" text box to focus it.
        await self._click_region(_EMAIL_ADDRESS_FIELD)
        await asyncio.sleep(0.5)

        delay = get_random_delay(100)

        # Select all existing text in the email address field.
        await self._driver.press_key([Key.CONTROL_OR_META, "a"], delay)
        await asyncio.sleep(0.5)

        # Clear the selected text.
        await self._driver.press_key(Key.BACKSPACE, delay)
        await asyncio.sleep(0.5)

        # Enter an email address in the text box.
        await self._driver.type_key(email, delay)
        await asyncio.sleep(0.5)

        # Click the "Send Code" button.
        await self._click_region(_SEND_CODE_BUTTON)
        await asyncio.sleep(0.1)
