import datetime
import tomllib
from collections.abc import Iterable, Sequence
from pathlib import Path
from typing import Final, Self

import cv2
import numpy as np

from majsoulrpa.common import TimeoutType
from majsoulrpa.presentation.presentation_base import Timeout

from .browser import STD_HEIGHT, STD_WIDTH, BrowserBase

MIN_ZOOM_RATIO: Final[float] = 2.0 / 3
MAX_ZOOM_RATIO: Final[float] = 2.0

_STD_EDGE_SIGMA: Final[float] = 0.2
_STD_THRESHOLD: Final[float] = 0.99

_PATH_TEMPLATE: Final[Path] = Path(__file__).parents[1]


def screenshot_to_opencv(screenshot_bytes: bytes) -> np.ndarray:
    img_array = np.frombuffer(screenshot_bytes, np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)


class Template:

    def __init__(  # noqa: PLR0913
        self, path: Path, zoom_ratio: float, *,
        left: int = 0, top: int = 0,
        width: int = STD_WIDTH, height: int = STD_HEIGHT,
        threshold: float = _STD_THRESHOLD,
    ) -> None:
        if zoom_ratio < MIN_ZOOM_RATIO or zoom_ratio > MAX_ZOOM_RATIO:
            msg = (
                "Zoom ratio is only supported "
                f"from {MIN_ZOOM_RATIO}x to {MAX_ZOOM_RATIO}x."
            )
            raise ValueError(msg)

        self._path = path
        self._zoom_ratio = zoom_ratio
        self._left = int(left * zoom_ratio)
        self._right = int((left + width)*zoom_ratio)
        self._top = int(top * zoom_ratio)
        self._bottom = int((top + height)*zoom_ratio)
        self._width = int(width * zoom_ratio)
        self._height = int(height * zoom_ratio)
        self._threshold = threshold

        templ = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if templ is None:
            msg = "Failed to open template image file."
            raise ValueError(msg)
        if templ.shape[0] == 0:
            msg = "The height of the template is equal to 0."
            raise ValueError(msg)
        if templ.shape[1] == 0:
            msg = "The width of the template is equal to 0."
            raise ValueError(msg)

        self._templ = cv2.resize(templ, None, fx=zoom_ratio, fy=zoom_ratio)

    @property
    def img_width(self) -> int:
        return self._templ.shape[1]

    @property
    def img_height(self) -> int:
        return self._templ.shape[0]

    @property
    def threshold(self) -> float:
        return self._threshold

    @classmethod
    def open_file(cls, name_or_path: str | Path, zoom_ratio: float) -> Self:  # noqa: C901, PLR0912
        if isinstance(name_or_path, str):
            path = _PATH_TEMPLATE / Path(name_or_path)
        else:
            path = _PATH_TEMPLATE / name_or_path

        if path.suffix == ".toml":
            pass
        elif path.suffix == ".png":
            if path.exists():
                return cls(path, zoom_ratio)
        elif path.suffix == "":
            if (p := path.with_suffix(".toml")).exists():
                path = p
            elif (p := path.with_suffix(".png")).exists():
                return cls(p, zoom_ratio)
            else:
                msg = f"{name_or_path}: an invalid template."
                raise ValueError(msg)
        else:
            msg = f"{name_or_path}: an invalid template."
            raise ValueError(msg)

        if not path.exists():
            msg = f"{path}: does not exist."
            raise ValueError(msg)

        with path.open("rb") as f:
            config = tomllib.load(f)

        if "path" in config:
            png_path_str: str = config["path"]
            if png_path_str.startswith("./"):
                png_path = path.parent / png_path_str
            else:
                png_path = Path(png_path_str)
            del config["path"]
        else:
            png_path = path.with_suffix(".png")

        if not png_path.exists():
            msg = f"{path}: does not exist."
            raise RuntimeError(msg)

        return cls(png_path, zoom_ratio, **config)

    def best_template_match(self, screenshot: bytes) -> tuple[int, int, float]:
        image = screenshot_to_opencv(screenshot)
        image = image[self._top:self._bottom, self._left:self._right, :]

        if image.shape[0] < self._templ.shape[0]:
            msg = (
                f"The height of the screenshot ({image.shape[0]}) is smaller"
                f"than the template's ({self._templ.shape[0]})."
            )
            raise ValueError(msg)
        if image.shape[1] < self._templ.shape[1]:
            msg = (
                f"The width of the screenshot ({image.shape[1]}) is smaller"
                f" than the template's ({self._templ.shape[1]})."
            )
            raise ValueError(msg)

        result1 = cv2.matchTemplate(image, self._templ, cv2.TM_CCOEFF_NORMED)
        result2 = cv2.matchTemplate(image, self._templ, cv2.TM_SQDIFF_NORMED)
        _, max_val1, _, max_loc1 = cv2.minMaxLoc(result1)
        min_val2, _, min_loc2, _ = cv2.minMaxLoc(result2)

        if max_val1 >= (1.0 - min_val2):
            argmax_x, argmax_y = max_loc1
            max_score = max_val1
        else:
            argmax_x, argmax_y = min_loc2
            max_score = 1.0 - min_val2

        return (self._left + argmax_x, self._top + argmax_y, max_score)

    def match(self, screenshot: bytes) -> bool:
        _, _, score = self.best_template_match(screenshot)
        return score >= self._threshold

    def wait_until(
        self, browser: BrowserBase, deadline: datetime.datetime,
    ) -> None:
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = f"Timeout in waiting {self._path}"
                raise Timeout(msg, browser.get_screenshot())
            if self.match(browser.get_screenshot()):
                break

    def wait_for(self, browser: BrowserBase, timeout: TimeoutType) -> None:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        deadline = datetime.datetime.now(datetime.UTC) + timeout
        self.wait_until(browser, deadline)

    def click(
        self, browser: BrowserBase, edge_sigma: float = _STD_EDGE_SIGMA,
    ) -> None:
        x, y, _ = self.best_template_match(browser.get_screenshot())
        browser.click_region(
            x, y, self._templ.shape[1], self._templ.shape[0], edge_sigma,
        )

    def wait_until_then_click(
        self, browser: BrowserBase, deadline: datetime.datetime,
        edge_sigma: float = _STD_EDGE_SIGMA,
    ) -> None:
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = f"Timeout in waiting {self._path}"
                raise Timeout(msg, browser.get_screenshot())
            x, y, score = self.best_template_match(browser.get_screenshot())
            if score >= self._threshold:
                break

        browser.click_region(
            x, y, self._templ.shape[1], self._templ.shape[0], edge_sigma,
        )

    def wait_for_then_click(
        self, browser: BrowserBase, timeout: TimeoutType,
        edge_sigma: float = _STD_EDGE_SIGMA,
    ) -> None:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)

        deadline = datetime.datetime.now(datetime.UTC) + timeout
        self.wait_until_then_click(browser, deadline, edge_sigma)

    @staticmethod
    def match_one_of(
        screenshot: bytes, templates: Sequence[str | Path], zoom_ratio: float,
    ) -> int:
        for i in range(len(templates)):
            template = Template.open_file(templates[i], zoom_ratio)
            if template.match(screenshot):
                return i
        return -1

    @staticmethod
    def wait_until_one_of_then_click(
        templates: Iterable["Template"], browser: BrowserBase,
        deadline: datetime.datetime, edge_sigma: float = _STD_EDGE_SIGMA,
    ) -> None:
        while True:
            if datetime.datetime.now(datetime.UTC) > deadline:
                msg = "Timeout"
                raise Timeout(msg, browser.get_screenshot())

            screenshot = browser.get_screenshot()
            for template in templates:
                x, y, score = template.best_template_match(screenshot)
                if score >= template.threshold:
                    browser.click_region(
                        x, y,
                        template.img_width, template.img_height,
                        edge_sigma,
                    )
                    return

    @staticmethod
    def wait_for_one_of_then_click(
        templates: Iterable["Template"], browser: BrowserBase,
        timeout: TimeoutType, edge_sigma: float = _STD_EDGE_SIGMA,
    ) -> None:
        if isinstance(timeout, int | float):
            timeout = datetime.timedelta(seconds=timeout)
        deadline = datetime.datetime.now(datetime.UTC) + timeout
        Template.wait_until_one_of_then_click(
            templates, browser, deadline, edge_sigma,
        )
