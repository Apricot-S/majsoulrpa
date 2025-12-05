import asyncio

from majsoulrpa import browser
from majsoulrpa.browser.driver import Key
from majsoulrpa.presentation.base import Presentation, PresentationType
from majsoulrpa.presentation.delay import get_random_delay
from majsoulrpa.presentation.region import Region


class LoginPresentation(Presentation):
    _LOGIN_BUTTON = Region(1290, 418, 410, 100)  # TODO: 後で画像認識に変える
    _EMAIL_ADDRESS_FIELD = Region(365, 385, 200, 30)
    _SEND_CODE_BUTTON = Region(850, 500, 190, 70)

    def __init__(self, driver: browser.DriverBase) -> None:
        super().__init__(driver)

    @staticmethod
    def get_type() -> PresentationType:
        return PresentationType.LOGIN

    @classmethod
    async def _detect(cls, driver: browser.DriverBase) -> bool:
        await asyncio.sleep(0.01)  # Dummy 正式な検出処理を入れたら不要
        return True

    async def _pre_dispatch(self) -> None:
        await self._init_resolution()
        # Clicking the "Login" button ensures the email input field
        # appears. If it is already visible, the click has no effect but
        # causes no issues, so we always perform the click for
        # simplicity.
        await self._click_region(LoginPresentation._LOGIN_BUTTON)
        await asyncio.sleep(0.5)

    async def enter_email_address(self, email: str) -> None:
        # Click the "Enter email address" text box to focus it.
        await self._click_region(LoginPresentation._EMAIL_ADDRESS_FIELD)
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
        await self._click_region(LoginPresentation._SEND_CODE_BUTTON)
        await asyncio.sleep(0.1)
