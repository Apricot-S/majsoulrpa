from abc import ABC, abstractmethod
from typing import override

import cv2
import numpy as np
from cv2.typing import MatLike

from majsoulrpa.presentation.region import Region
from majsoulrpa.presentation.template.config import Config
from majsoulrpa.presentation.template.image import ImageBase


class MatcherBase(ABC):
    @abstractmethod
    def match(self, screen: bytes, scale: float) -> Region | None:
        pass


def _resize_image(original: MatLike, scale: float) -> MatLike:
    return cv2.resize(original, None, fx=scale, fy=scale)


def _screenshot_to_mat(screenshot: bytes) -> MatLike:
    img_array = np.frombuffer(screenshot, np.uint8)
    img_mat = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img_mat is None:
        msg = "failed to decode screenshot bytes into an image"
        raise RuntimeError(msg)
    return img_mat


class Matcher(MatcherBase):
    def __init__(self, image: ImageBase[MatLike], config: Config) -> None:
        self._image = image
        self._config = config

    @override
    def match(self, screen: bytes, scale: float) -> Region | None:
        template = _resize_image(self._image.get_image(), scale)
        screen_mat = _screenshot_to_mat(screen)

        region = self._config.region
        margin = self._config.margin
        x0 = int(scale * (region.left - margin.left))
        y0 = int(scale * (region.top - margin.top))
        x1 = int(scale * (region.left + region.width + margin.right))
        y1 = int(scale * (region.top + region.height + margin.bottom))
        roi = screen_mat[y0:y1, x0:x1]

        result1 = cv2.matchTemplate(roi, template, cv2.TM_CCOEFF_NORMED)
        result2 = cv2.matchTemplate(roi, template, cv2.TM_SQDIFF_NORMED)
        _, max_val1, _, max_loc1 = cv2.minMaxLoc(result1)
        min_val2, _, min_loc2, _ = cv2.minMaxLoc(result2)

        if max_val1 >= (1.0 - min_val2):
            argmax_x, argmax_y = max_loc1
            max_score = max_val1
        else:
            argmax_x, argmax_y = min_loc2
            max_score = 1.0 - min_val2

        if max_score < self._config.settings.threshold:
            return None

        left = x0 + argmax_x
        top = y0 + argmax_y
        width = scale * self._config.region.width
        height = scale * self._config.region.height

        return Region(left=left, top=top, width=width, height=height)
