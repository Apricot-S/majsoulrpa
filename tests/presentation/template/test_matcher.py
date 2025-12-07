from typing import override

import cv2
import numpy as np

from majsoulrpa.presentation.template import Config, ImageBase, Matcher, config


class DummyImage(ImageBase):
    def __init__(self, mat: np.ndarray) -> None:
        self._mat = mat

    @override
    def get_scaled(self, scale: float) -> cv2.typing.MatLike:
        return self._mat


def ndarray_to_png_bytes(arr: np.ndarray) -> bytes:
    success, encoded = cv2.imencode(".png", arr)
    if not success:
        msg = "PNG encoding failed"
        raise ValueError(msg)
    return encoded.tobytes()


def test_matcher_returns_correct_coordinates_roi_origin() -> None:
    screen_array = np.zeros((100, 100, 3), dtype=np.uint8)
    screen_array[50:100, 0:50] = 255
    screen_array[50:60, 0:10] = 0
    screen = ndarray_to_png_bytes(screen_array)

    template = np.ones((50, 50, 3), dtype=np.uint8) * 255
    template[0:10, 0:10] = 0

    cfg = Config(
        region=config.Region(left=0, top=0, width=100, height=100),
        margin=config.Margin(left=0, right=0, top=0, bottom=0),
        settings=config.Settings(threshold=0.999),
    )

    matcher = Matcher(DummyImage(template), cfg)
    assert matcher.match(screen, scale=1.0) == (0, 50)


def test_matcher_returns_correct_coordinates_roi_offset() -> None:
    screen_array = np.zeros((512, 512, 3), dtype=np.uint8)
    screen_array[255:512, 255:512] = 255
    screen_array[255:265, 255:265] = 0
    screen = ndarray_to_png_bytes(screen_array)

    template = np.ones((256, 256, 3), dtype=np.uint8) * 255
    template[0:10, 0:10] = 0

    cfg = Config(
        region=config.Region(left=200, top=100, width=312, height=412),
        margin=config.Margin(left=0, right=0, top=0, bottom=0),
        settings=config.Settings(threshold=0.999),
    )

    matcher = Matcher(DummyImage(template), cfg)
    assert matcher.match(screen, scale=1.0) == (255, 255)


def test_matcher_returns_none_when_below_threshold() -> None:
    screen_array = np.zeros((512, 512, 3), dtype=np.uint8)
    screen_array[255:512, 0:255] = 255
    screen_array[255:265, 0:10] = 128

    screen = ndarray_to_png_bytes(screen_array)

    template = np.ones((256, 256, 3), dtype=np.uint8) * 255
    template[0:10, 0:10] = 0

    cfg = Config(
        region=config.Region(left=0, top=0, width=512, height=512),
        margin=config.Margin(left=0, right=0, top=0, bottom=0),
        settings=config.Settings(threshold=0.999),
    )

    matcher = Matcher(DummyImage(template), cfg)
    assert matcher.match(screen, scale=1.0) is None
