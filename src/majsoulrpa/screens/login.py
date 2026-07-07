from typing import override

from majsoulrpa.assets.templates.login import (
    LOGIN_1_SETTINGS_PATH,
    LOGIN_1_TEMPLATE_PATH,
    YOSTAR_LOGO_SETTINGS_PATH,
    YOSTAR_LOGO_TEMPLATE_PATH,
)
from majsoulrpa.presentation.region import Region
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import Screen, ScreenDetectionSpec

LOGIN_1_TEMPLATE = load_png_template_matcher(
    template_path=LOGIN_1_TEMPLATE_PATH,
    settings_path=LOGIN_1_SETTINGS_PATH,
)
YOSTAR_LOGO_TEMPLATE = load_png_template_matcher(
    template_path=YOSTAR_LOGO_TEMPLATE_PATH,
    settings_path=YOSTAR_LOGO_SETTINGS_PATH,
)


class LoginScreen(Screen):
    EMAIL_ADDRESS_REGION = Region(left=770, top=430, width=138, height=20)
    SEND_REGION = Region(left=1102, top=508, width=40, height=22)
    VERIFICATION_CODE_REGION = Region(left=768, top=508, width=100, height=20)

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=LOGIN_1_TEMPLATE.matches)

    @override
    async def before_callback(self) -> None:
        await self.click_if_match(LOGIN_1_TEMPLATE)

    async def enter_email_address(self, email_address: str) -> None:
        await self.fill_region(self.EMAIL_ADDRESS_REGION, email_address)
