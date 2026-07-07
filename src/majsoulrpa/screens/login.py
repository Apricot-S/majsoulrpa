from pathlib import Path
from typing import override

import cv2
import numpy as np

from majsoulrpa.presentation.region import Region
from majsoulrpa.presentation.template import (
    TemplateMatcher,
    TemplateMatchSettings,
)
from majsoulrpa.screens.base import (
    Screen,
    ScreenDetectionSpec,
    TemplateMatchResult,
)

_ASSET_DIR = Path(__file__).parents[1] / "assets" / "templates" / "login"
_LOGIN_1_TEMPLATE_PATH = _ASSET_DIR / "login-1.png"
_LOGIN_1_SETTINGS_PATH = _ASSET_DIR / "login-1.toml"


def _read_grayscale_png(path: Path) -> np.ndarray:
    image = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if image is None:
        msg = f"PNG image could not be decoded: {path}"
        raise ValueError(msg)
    return image


def _decode_grayscale_png(payload: bytes) -> np.ndarray:
    encoded = np.frombuffer(payload, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    if image is None:
        msg = "PNG image could not be decoded."
        raise ValueError(msg)
    return image


class PngTemplateMatcher:
    def __init__(self, matcher: TemplateMatcher) -> None:
        self._matcher = matcher

    def matches(self, screenshot: object) -> bool:
        if not isinstance(screenshot, bytes):
            msg = "LoginScreen screenshot must be PNG bytes."
            raise TypeError(msg)
        return self._matcher.matches(_decode_grayscale_png(screenshot))

    def match(self, screenshot: object) -> TemplateMatchResult:
        if not isinstance(screenshot, bytes):
            msg = "LoginScreen screenshot must be PNG bytes."
            raise TypeError(msg)
        return self._matcher.match(_decode_grayscale_png(screenshot))


LOGIN_1_TEMPLATE = PngTemplateMatcher(
    TemplateMatcher(
        _read_grayscale_png(_LOGIN_1_TEMPLATE_PATH),
        TemplateMatchSettings.from_toml_text(
            _LOGIN_1_SETTINGS_PATH.read_text(encoding="utf-8"),
        ),
    ),
)


class LoginScreen(Screen):
    email_address_region = Region(left=0, top=0, width=1, height=1)

    @classmethod
    @override
    def detection_spec(cls) -> ScreenDetectionSpec:
        return ScreenDetectionSpec(predicate=LOGIN_1_TEMPLATE.matches)

    @override
    async def before_callback(self) -> None:
        await self.click_if_match(LOGIN_1_TEMPLATE)

    async def enter_email_address(self, email_address: str) -> None:
        await self.fill_region(self.email_address_region, email_address)
