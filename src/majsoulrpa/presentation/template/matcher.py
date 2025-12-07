from abc import ABC, abstractmethod
from typing import override

import cv2
import numpy as np

from majsoulrpa.presentation.template import Config, ImageBase


class MatcherBase(ABC):
    @abstractmethod
    def match(self, screen: bytes, scale: float) -> tuple[int, int] | None:
        pass


def _screenshot_to_mat(screenshot_bytes: bytes) -> np.ndarray:
    img_array = np.frombuffer(screenshot_bytes, np.uint8)
    img_mat = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
    if img_mat is None:
        msg = "failed to decode screenshot bytes into an image"
        raise RuntimeError(msg)
    return img_mat


class Matcher(MatcherBase):
    def __init__(self, image: ImageBase, config: Config) -> None:
        self._image = image
        self._config = config

    @override
    def match(self, screen: bytes, scale: float) -> tuple[int, int] | None:
        template = self._image.get_scaled(scale)
        screen_mat = _screenshot_to_mat(screen)

        region = self._config.region
        margin = self._config.margin
        x0 = region.left - margin.left
        y0 = region.top - margin.top
        x1 = region.left + region.width + margin.right
        y1 = region.top + region.height + margin.bottom
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
        return (x0 + argmax_x, y0 + argmax_y)
