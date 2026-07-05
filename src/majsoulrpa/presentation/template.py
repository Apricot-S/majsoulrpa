import tomllib
from dataclasses import dataclass
from typing import Annotated, cast

import cv2
import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa.presentation.region import Region

BASE_VIEWPORT_WIDTH = 1920
BASE_VIEWPORT_HEIGHT = 1080

NonNegativeCoordinate = Annotated[float, Field(ge=0)]
PositiveSize = Annotated[float, Field(gt=0)]
MatchThreshold = Annotated[float, Field(ge=0, le=1)]


@dataclass(frozen=True)
class TemplateMatchResult:
    score: float
    region: Region


class RegionConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    left: NonNegativeCoordinate
    top: NonNegativeCoordinate
    width: PositiveSize
    height: PositiveSize

    def to_region(self) -> Region:
        return Region(
            left=self.left,
            top=self.top,
            width=self.width,
            height=self.height,
        )


class MarginConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    top: NonNegativeCoordinate
    right: NonNegativeCoordinate
    bottom: NonNegativeCoordinate
    left: NonNegativeCoordinate


class MatchConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    threshold: MatchThreshold


class TemplateMatchSettings(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    region: RegionConfig
    margin: MarginConfig
    match: MatchConfig

    @classmethod
    def from_toml_text(cls, text: str) -> "TemplateMatchSettings":
        return cls.model_validate(tomllib.loads(text))


class TemplateMatcher:
    def __init__(
        self,
        template: NDArray[np.uint8],
        settings: TemplateMatchSettings,
    ) -> None:
        self._template = template
        self._settings = settings
        self._validate_template_size()

    def match(self, screenshot: NDArray[np.uint8]) -> TemplateMatchResult:
        scale = self._calculate_scale(screenshot)
        search_region = self._scaled_search_region(scale)
        self._validate_search_region(screenshot, search_region)
        scaled_template = self._scaled_template(scale)
        search_image = screenshot[
            round(search_region.top) : round(search_region.bottom),
            round(search_region.left) : round(search_region.right),
        ]
        match_result = cv2.matchTemplate(
            search_image,
            scaled_template,
            cv2.TM_CCOEFF_NORMED,
        )
        _, max_score, _, max_location = cv2.minMaxLoc(match_result)
        match_left = search_region.left + max_location[0]
        match_top = search_region.top + max_location[1]

        return TemplateMatchResult(
            score=max_score,
            region=Region(
                left=match_left,
                top=match_top,
                width=scaled_template.shape[1],
                height=scaled_template.shape[0],
            ),
        )

    def matches(self, screenshot: NDArray[np.uint8]) -> bool:
        return self.match(screenshot).score >= self._settings.match.threshold

    def _validate_template_size(self) -> None:
        template_height, template_width = self._template.shape[:2]
        region = self._settings.region
        if template_width != round(region.width) or template_height != round(
            region.height
        ):
            msg = "template size must match configured region size."
            raise ValueError(msg)

    @staticmethod
    def _calculate_scale(screenshot: NDArray[np.uint8]) -> float:
        screenshot_height, screenshot_width = screenshot.shape[:2]
        scale_x = screenshot_width / BASE_VIEWPORT_WIDTH
        scale_y = screenshot_height / BASE_VIEWPORT_HEIGHT
        if scale_x != scale_y:
            msg = "screenshot aspect ratio must match 16:9."
            raise ValueError(msg)
        return scale_x

    def _scaled_template(self, scale: float) -> NDArray[np.uint8]:
        if scale == 1:
            return self._template

        region = self._settings.region.to_region()
        width = self._scaled_size(region.width, scale)
        height = self._scaled_size(region.height, scale)
        resized = cv2.resize(
            self._template,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )
        return cast("NDArray[np.uint8]", resized)

    def _scaled_search_region(self, scale: float) -> Region:
        region = self._settings.region.to_region()
        margin = self._settings.margin
        left = region.left - margin.left
        top = region.top - margin.top
        width = region.width + margin.left + margin.right
        height = region.height + margin.top + margin.bottom

        return Region(
            left=round(left * scale),
            top=round(top * scale),
            width=self._scaled_size(width, scale),
            height=self._scaled_size(height, scale),
        )

    @staticmethod
    def _scaled_size(size: float, scale: float) -> int:
        scaled_size = round(size * scale)
        if scaled_size <= 0:
            msg = "scaled region size must be positive."
            raise ValueError(msg)
        return scaled_size

    @staticmethod
    def _validate_search_region(
        screenshot: NDArray[np.uint8],
        search_region: Region,
    ) -> None:
        screenshot_height, screenshot_width = screenshot.shape[:2]
        if (
            search_region.left < 0
            or search_region.top < 0
            or search_region.right > screenshot_width
            or search_region.bottom > screenshot_height
        ):
            msg = "search region must fit inside screenshot."
            raise ValueError(msg)
