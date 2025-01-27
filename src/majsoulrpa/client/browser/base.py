import random
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from fractions import Fraction
from logging import getLogger
from typing import Final

logger = getLogger(__name__)

URL_MAJSOUL: Final[str] = "https://game.mahjongsoul.com/"

STD_WIDTH: Final[int] = 1920
STD_HEIGHT: Final[int] = 1080
MIN_WIDTH: Final[int] = STD_WIDTH * 2 // 3
MIN_HEIGHT: Final[int] = STD_HEIGHT * 2 // 3
MAX_WIDTH: Final[int] = STD_WIDTH * 2
MAX_HEIGHT: Final[int] = STD_HEIGHT * 2
ASPECT_RATIO: Final[Fraction] = Fraction(16, 9)


def validate_viewport_size(width: int, height: int) -> None:
    if (
        width < MIN_WIDTH
        or width > MAX_WIDTH
        or height < MIN_HEIGHT
        or height > MAX_HEIGHT
        or Fraction(width, height) != ASPECT_RATIO
    ):
        msg = (
            "Supported viewport sizes are "
            f"from {MIN_WIDTH} x {MIN_HEIGHT} "
            f"to {MAX_WIDTH} x {MAX_HEIGHT} and 16:9 aspect ratio."
        )
        raise ValueError(msg)


def validate_region(
    left: int,
    top: int,
    width: int,
    height: int,
    viewport_width: int,
    viewport_height: int,
) -> None:
    if (
        left < 0
        or top < 0
        or width <= 0
        or height <= 0
        or left >= viewport_width
        or top >= viewport_height
        or width > (viewport_width - left)
        or height > (viewport_height - top)
    ):
        msg = (
            "A click was requested into an invalid area."
            f" {left=}, {top=}, {width=}, {height=}"
        )
        raise ValueError(msg)


def get_random_point_in_region(
    left: int,
    top: int,
    width: int,
    height: int,
    edge_sigma: float = 0.2,
) -> tuple[int, int]:
    """Return random point in region.

    This function does not validate parameters.
    """

    def _get_point_impl(distance_origin: int, length_region: int) -> int:
        mu = distance_origin + length_region / 2.0
        sigma = (mu - distance_origin) / edge_sigma
        while True:
            p = random.normalvariate(mu, sigma)
            p = round(p)
            if distance_origin < p < (distance_origin + length_region):
                break
        return p

    x = _get_point_impl(left, width)
    y = _get_point_impl(top, height)

    return (x, y)


class BrowserBase(metaclass=ABCMeta):
    @abstractmethod
    async def get_zoom_ratio(self) -> float:
        pass

    @abstractmethod
    async def refresh(self) -> None:
        pass

    @abstractmethod
    async def write(self, text: str, delay: float | None = None) -> None:
        pass

    @abstractmethod
    async def press(self, keys: str | Iterable[str]) -> None:
        pass

    @abstractmethod
    async def press_hotkey(self, *args: str) -> None:
        pass

    @abstractmethod
    async def move_to_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        pass

    @abstractmethod
    async def scroll(self, clicks: int) -> None:
        pass

    @abstractmethod
    async def click_region(
        self,
        left: int,
        top: int,
        width: int,
        height: int,
        edge_sigma: float = 2.0,
    ) -> None:
        pass

    @abstractmethod
    async def get_screenshot(self) -> bytes:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass
