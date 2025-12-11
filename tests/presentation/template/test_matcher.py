from typing import override

import cv2
import numpy as np
from cv2.typing import MatLike

from majsoulrpa.presentation.region import Region
from majsoulrpa.presentation.template import Config, ImageBase, Matcher, config


class DummyImage(ImageBase):
    def __init__(self, mat: MatLike) -> None:
        self._mat = mat

    @override
    def get_image(self) -> MatLike:
        return self._mat


def ndarray_to_png_bytes(arr: MatLike) -> bytes:
    success, encoded = cv2.imencode(".png", arr)
    if not success:
        msg = "PNG encoding failed"
        raise ValueError(msg)
    return encoded.tobytes()


def test_matcher_returns_correct_coordinates_not_scaled() -> None:
    screen_array = np.zeros((100, 100, 3), dtype=np.uint8)
    screen_array[50:100, 0:50] = 255
    screen_array[50:60, 0:10] = 0
    screen = ndarray_to_png_bytes(screen_array)

    template = np.ones((50, 50, 3), dtype=np.uint8) * 255
    template[0:10, 0:10] = 0

    cfg = Config(
        region=config.Region(left=0, top=50, width=50, height=50),
        margin=config.Margin(left=0, right=0, top=0, bottom=0),
        settings=config.Settings(threshold=0.99),
    )

    matcher = Matcher(DummyImage(template), cfg)
    assert matcher.match(screen, scale=1.0) == Region(0, 50, 50, 50)


def test_matcher_returns_correct_coordinates_scaled() -> None:
    screen_array = np.zeros((200, 200, 3), dtype=np.uint8)
    screen_array[100:200, 0:100] = 255
    screen_array[100:120, 0:20] = 0
    screen = ndarray_to_png_bytes(screen_array)

    # Template image is defined in pre-scaled size
    template = np.ones((50, 50, 3), dtype=np.uint8) * 255
    template[0:10, 0:10] = 0

    # Config also uses pre-scaled values
    cfg = Config(
        region=config.Region(left=0, top=50, width=50, height=50),
        margin=config.Margin(left=0, right=0, top=0, bottom=0),
        settings=config.Settings(threshold=0.99),
    )

    matcher = Matcher(DummyImage(template), cfg)
    assert matcher.match(screen, scale=2.0) == Region(0, 100, 100, 100)


def test_matcher_returns_none_when_not_match() -> None:
    screen_array = np.zeros((100, 100, 3), dtype=np.uint8)
    screen_array[50:100, 0:50] = 255
    screen = ndarray_to_png_bytes(screen_array)

    template = np.ones((50, 50, 3), dtype=np.uint8) * 255
    template[0:10, 0:10] = 0

    cfg = Config(
        region=config.Region(left=0, top=50, width=50, height=50),
        margin=config.Margin(left=0, right=0, top=0, bottom=0),
        settings=config.Settings(threshold=0.99),
    )

    matcher = Matcher(DummyImage(template), cfg)
    assert matcher.match(screen, scale=1.0) is None
