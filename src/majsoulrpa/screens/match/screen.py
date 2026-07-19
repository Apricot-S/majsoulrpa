from typing import override

from majsoulrpa.assets.templates.match import (
    SEAT_INDICATOR_SETTINGS_PATH,
    SEAT_INDICATOR_TEMPLATE_PATHS,
)
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import Screen, ScreenDetectionSpec


class MatchScreen(Screen):
    SEAT_INDICATOR_TEMPLATES = tuple(
        load_png_template_matcher(
            template_path=template_path,
            settings_path=SEAT_INDICATOR_SETTINGS_PATH,
        )
        for template_path in SEAT_INDICATOR_TEMPLATE_PATHS
    )

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=cls._matches_seat_indicator)

    @override
    async def before_callback(self) -> None:
        pass

    @classmethod
    def _matches_seat_indicator(cls, screenshot: object) -> bool:
        return any(
            template.matches(screenshot)
            for template in cls.SEAT_INDICATOR_TEMPLATES
        )
