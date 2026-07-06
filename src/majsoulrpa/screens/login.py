from typing import override

from majsoulrpa.presentation.region import Region
from majsoulrpa.screens.base import Screen, ScreenDetectionSpec


def _login_template_matches(_screenshot: object) -> bool:
    msg = "LoginScreen template matcher is not configured."
    raise RuntimeError(msg)


class LoginScreen(Screen):
    email_address_region = Region(left=0, top=0, width=1, height=1)

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=_login_template_matches)

    async def enter_email_address(self, email_address: str) -> None:
        await self.fill_region(self.email_address_region, email_address)
