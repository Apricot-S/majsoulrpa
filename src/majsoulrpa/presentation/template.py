import tomllib
from dataclasses import dataclass
from importlib.resources.abc import Traversable
from math import isfinite
from pathlib import Path
from typing import Annotated, cast

import cv2
import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa.constants import BASE_VIEWPORT_HEIGHT, BASE_VIEWPORT_WIDTH
from majsoulrpa.presentation.region import Region

NonNegativeCoordinate = Annotated[float, Field(ge=0)]
PositiveSize = Annotated[float, Field(gt=0)]
MatchThreshold = Annotated[float, Field(ge=0, le=1)]
_GRAYSCALE_IMAGE_DIMENSIONS = 2
_PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


@dataclass(frozen=True)
class TemplateMatchResult:
    score: float
    region: Region

    def __post_init__(self) -> None:
        if not isfinite(self.score) or not 0.0 <= self.score <= 1.0:
            msg = "template match score must be finite and between 0 and 1."
            raise ValueError(msg)


class _TemplateConfigModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        allow_inf_nan=False,
    )


class RegionConfig(_TemplateConfigModel):
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


class MarginConfig(_TemplateConfigModel):
    top: NonNegativeCoordinate
    right: NonNegativeCoordinate
    bottom: NonNegativeCoordinate
    left: NonNegativeCoordinate


class MatchConfig(_TemplateConfigModel):
    threshold: MatchThreshold


class TemplateMatchSettings(_TemplateConfigModel):
    region: RegionConfig
    margin: MarginConfig
    match: MatchConfig

    @classmethod
    def from_toml_text(cls, text: str) -> "TemplateMatchSettings":
        return cls.model_validate(tomllib.loads(text))

    @classmethod
    def from_toml_file(
        cls,
        path: Path | Traversable,
    ) -> "TemplateMatchSettings":
        with path.open("rb") as fp:
            return cls.model_validate(tomllib.load(fp))


class TemplateMatcher:
    def __init__(
        self,
        template: NDArray[np.uint8],
        settings: TemplateMatchSettings,
    ) -> None:
        _validate_grayscale_image(template, name="template")
        self._template = template
        self._settings = settings
        self._validate_template_size()

    def match(self, screenshot: NDArray[np.uint8]) -> TemplateMatchResult:
        _validate_grayscale_image(screenshot, name="screenshot")
        scale = self._calculate_scale(screenshot)
        search_region = self._scaled_search_region(scale)
        self._validate_search_region(screenshot, search_region)
        scaled_template = self._scaled_template(scale)
        search_image = screenshot[
            round(search_region.top) : round(search_region.bottom),
            round(search_region.left) : round(search_region.right),
        ]
        ccoeff_match_result = cv2.matchTemplate(
            search_image,
            scaled_template,
            cv2.TM_CCOEFF_NORMED,
        )
        _, ccoeff_score, _, ccoeff_location = cv2.minMaxLoc(
            ccoeff_match_result,
        )
        sqdiff_match_result = cv2.matchTemplate(
            search_image,
            scaled_template,
            cv2.TM_SQDIFF_NORMED,
        )
        sqdiff_min_score, _, sqdiff_location, _ = cv2.minMaxLoc(
            sqdiff_match_result,
        )
        sqdiff_score = 1.0 - sqdiff_min_score

        if ccoeff_score >= sqdiff_score:
            score = ccoeff_score
            location = ccoeff_location
        else:
            score = sqdiff_score
            location = sqdiff_location

        match_left = search_region.left + location[0]
        match_top = search_region.top + location[1]

        return TemplateMatchResult(
            score=score,
            region=Region(
                left=match_left,
                top=match_top,
                width=scaled_template.shape[1],
                height=scaled_template.shape[0],
            ),
        )

    def find(
        self,
        screenshot: NDArray[np.uint8],
    ) -> TemplateMatchResult | None:
        result = self.match(screenshot)
        if result.score < self._settings.match.threshold:
            return None
        return result

    def matches(self, screenshot: NDArray[np.uint8]) -> bool:
        return self.find(screenshot) is not None

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

        region = self._settings.region
        width = self._scaled_size(region.width, scale)
        height = self._scaled_size(region.height, scale)
        resized = cv2.resize(
            self._template,
            (width, height),
            interpolation=cv2.INTER_LINEAR,
        )
        return cast("NDArray[np.uint8]", resized)

    def _scaled_search_region(self, scale: float) -> Region:
        region = self._settings.region
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


class PngTemplateMatcher:
    def __init__(self, matcher: TemplateMatcher) -> None:
        self._matcher = matcher

    def match(self, screenshot: object) -> TemplateMatchResult:
        if not isinstance(screenshot, bytes):
            msg = "screenshot must be PNG bytes."
            raise TypeError(msg)
        return self._matcher.match(_decode_grayscale_png(screenshot))

    def find(self, screenshot: object) -> TemplateMatchResult | None:
        if not isinstance(screenshot, bytes):
            msg = "screenshot must be PNG bytes."
            raise TypeError(msg)
        return self._matcher.find(_decode_grayscale_png(screenshot))

    def matches(self, screenshot: object) -> bool:
        return self.find(screenshot) is not None


def load_png_template_matcher(
    *,
    template_path: Path | Traversable,
    settings_path: Path | Traversable,
) -> PngTemplateMatcher:
    return PngTemplateMatcher(
        TemplateMatcher(
            _read_grayscale_png(template_path),
            TemplateMatchSettings.from_toml_file(settings_path),
        ),
    )


def _read_grayscale_png(path: Path | Traversable) -> NDArray[np.uint8]:
    try:
        return _decode_grayscale_png(path.read_bytes())
    except ValueError as error:
        msg = f"PNG image could not be decoded: {path}"
        raise ValueError(msg) from error


def _decode_grayscale_png(payload: bytes) -> NDArray[np.uint8]:
    if not payload.startswith(_PNG_SIGNATURE):
        msg = "PNG image could not be decoded."
        raise ValueError(msg)
    encoded = np.frombuffer(payload, dtype=np.uint8)
    image = cv2.imdecode(encoded, cv2.IMREAD_GRAYSCALE)
    if image is None:
        msg = "PNG image could not be decoded."
        raise ValueError(msg)
    return cast("NDArray[np.uint8]", image)


def _validate_grayscale_image(image: NDArray[np.uint8], *, name: str) -> None:
    if image.ndim != _GRAYSCALE_IMAGE_DIMENSIONS:
        msg = f"{name} must be a 2D grayscale image."
        raise ValueError(msg)
    if image.dtype != np.uint8:
        msg = f"{name} dtype must be uint8."
        raise TypeError(msg)
    if image.size == 0:
        msg = f"{name} must not be empty."
        raise ValueError(msg)
