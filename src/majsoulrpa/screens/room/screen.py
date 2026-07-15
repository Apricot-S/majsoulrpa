from typing import override

from majsoulrpa.assets.templates.room import (
    ROOM_SIGN_SETTINGS_PATH,
    ROOM_SIGN_TEMPLATE_PATH,
)
from majsoulrpa.presentation.template import load_png_template_matcher
from majsoulrpa.screens.base import Screen, ScreenDetectionSpec


class RoomScreen(Screen):
    ROOM_SIGN_TEMPLATE = load_png_template_matcher(
        template_path=ROOM_SIGN_TEMPLATE_PATH,
        settings_path=ROOM_SIGN_SETTINGS_PATH,
    )

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=cls.ROOM_SIGN_TEMPLATE.matches)

    @override
    async def before_callback(self) -> None:
        pass
