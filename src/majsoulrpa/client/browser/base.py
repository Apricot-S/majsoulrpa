import random
from abc import ABCMeta, abstractmethod
from collections.abc import Iterable
from fractions import Fraction
from logging import getLogger
from typing import Final

logger = getLogger(__name__)

URL_MAJSOUL_JP: Final[str] = "https://game.mahjongsoul.com/"
"""The URL for the Mahjong Soul JP server."""

STD_WIDTH: Final[int] = 1920
"""The standard viewport width."""
STD_HEIGHT: Final[int] = 1080
"""The standard viewport height."""
MIN_WIDTH: Final[int] = STD_WIDTH * 2 // 3
"""The minimum allowed viewport width."""
MIN_HEIGHT: Final[int] = STD_HEIGHT * 2 // 3
"""The minimum allowed viewport height."""
MAX_WIDTH: Final[int] = STD_WIDTH * 2
"""The maximum allowed viewport width."""
MAX_HEIGHT: Final[int] = STD_HEIGHT * 2
"""The maximum allowed viewport height."""
ASPECT_RATIO: Final[Fraction] = Fraction(16, 9)
"""The required aspect ratio for the viewport."""


def validate_viewport_size(width: int, height: int) -> None:
    """Validates if a given viewport size is supported.

    Checks if the given viewport width and height are within the allowed
    range and have the correct aspect ratio.

    Args:
        width: The viewport width.
        height: The viewport height.

    Raises:
        ValueError: If the viewport size is not supported.
    """
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
    """Validates if a given region is within the bounds of a viewport.

    Checks if the given region, defined by its top-left corner
    (`left`, `top`) and dimensions (`width`, `height`), is within
    the bounds of the viewport with dimensions (`viewport_width`,
    `viewport_height`).

    Args:
        left: The x-coordinate of the region's top-left corner.
        top: The y-coordinate of the region's top-left corner.
        width: The width of the region.
        height: The height of the region.
        viewport_width: The viewport width.
        viewport_height: The viewport height.

    Raises:
        ValueError: If the specified region is invalid.
    """
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
            "An invalid region was specified."
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
    """Gets a random point in a given region.

    This function does not validate parameters.

    Args:
        left: The x-coordinate of the region's top-left corner.
        top: The y-coordinate of the region's top-left corner.
        width: The width of the region.
        height: The height of the region.
        edge_sigma: Controls the spread of points of the region.
            The smaller the `edge_sigma`, the larger the spread (sigma),
            causing points to be more widely distributed. Conversely,
            a larger `edge_sigma` results in a smaller spread (sigma),
            concentrating points closer to the center.
            Defaults to `0.2`.

    Returns:
        x, y-coordinates of a random point within the specified region.
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
    """An abstract base class for browser interactions."""

    @abstractmethod
    async def get_zoom_ratio(self) -> float:
        """Gets the zoom ratio of the viewport size.

        Returns:
            The zoom ratio of the current viewport size relative to the
                standard viewport size.
        """

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
        """Clicks a random point in a given region.

        Args:
            left: The x-coordinate of the region's top-left corner.
            top: The y-coordinate of the region's top-left corner.
            width: The width of the region.
            height: The height of the region.
            edge_sigma: Controls the spread of points of the region.
                The smaller the `edge_sigma`, the larger the spread
                (sigma), causing points to be more widely distributed.
                Conversely, a larger `edge_sigma` results in a smaller
                spread (sigma), concentrating points closer to the
                center. Defaults to 2.0.

        Raises:
            ValueError: If the specified region is invalid or
                `edge_sigma` is not positive.
        """

    @abstractmethod
    async def get_screenshot(self) -> bytes:
        """Captures a screenshot in PNG format.

        Returns:
            The screenshot as a PNG byte array.
        """

    @abstractmethod
    async def close(self) -> None:
        """Closes the browser."""
