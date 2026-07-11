import asyncio
from typing import override

from majsoulrpa.assets.templates.home import (
    EVENT_CLOSE_SETTINGS_PATH,
    EVENT_CLOSE_TEMPLATE_PATH,
    MAIL_CLOSE_SETTINGS_PATH,
    MAIL_CLOSE_TEMPLATE_PATH,
    NOTIFICATION_CLOSE_SETTINGS_PATH,
    NOTIFICATION_CLOSE_TEMPLATE_PATH,
    SUMMON_SETTINGS_PATH,
    SUMMON_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import Screen, ScreenDetectionSpec
from majsoulrpa.screens.errors import ScreenUnexpectedStateError


class HomeScreen(Screen):
    SUMMON_TEMPLATE = load_png_template_matcher(
        template_path=SUMMON_TEMPLATE_PATH,
        settings_path=SUMMON_SETTINGS_PATH,
    )
    NOTIFICATION_CLOSE_TEMPLATE = load_png_template_matcher(
        template_path=NOTIFICATION_CLOSE_TEMPLATE_PATH,
        settings_path=NOTIFICATION_CLOSE_SETTINGS_PATH,
    )
    EVENT_CLOSE_TEMPLATE = load_png_template_matcher(
        template_path=EVENT_CLOSE_TEMPLATE_PATH,
        settings_path=EVENT_CLOSE_SETTINGS_PATH,
    )
    MAIL_CLOSE_TEMPLATE = load_png_template_matcher(
        template_path=MAIL_CLOSE_TEMPLATE_PATH,
        settings_path=MAIL_CLOSE_SETTINGS_PATH,
    )

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=cls.SUMMON_TEMPLATE.matches)

    @override
    async def before_callback(self) -> None:
        close_templates = {
            "notification-close": self.NOTIFICATION_CLOSE_TEMPLATE,
            "event-close": self.EVENT_CLOSE_TEMPLATE,
            "mail-close": self.MAIL_CLOSE_TEMPLATE,
        }
        processed_templates: set[str] = set()
        while len(processed_templates) < len(close_templates):
            screenshot = await self.context.browser.screenshot()
            for name, template in close_templates.items():
                result = template.find(screenshot)
                if result is None:
                    continue

                if name in processed_templates:
                    msg = f"{name} was detected more than once."
                    raise ScreenUnexpectedStateError(msg, screenshot)

                await self._click_region(result.region)
                processed_templates.add(name)
                await asyncio.sleep(1.0)
                break
            else:
                return
