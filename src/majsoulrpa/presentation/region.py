import random
from dataclasses import dataclass

DEFAULT_EDGE_SIGMA = 0.2


@dataclass(frozen=True)
class Region:
    """Rectangular region defined by top-left corner and size.

    Attributes:
        left: X coordinate of the region's left edge.
        top: Y coordinate of the region's top edge.
        width: Width of the region.
        height: Height of the region.
    """

    left: float
    top: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.left < 0.0:
            msg = f"`Region.left` must be non-negative, got {self.left}"
            raise ValueError(msg)
        if self.top < 0.0:
            msg = f"`Region.top` must be non-negative, got {self.top}"
            raise ValueError(msg)
        if self.width <= 0.0:
            msg = f"`Region.width` must be positive, got {self.width}"
            raise ValueError(msg)
        if self.height <= 0.0:
            msg = f"`Region.height` must be positive, got {self.height}"
            raise ValueError(msg)

    def scale(self, factor: float) -> "Region":
        if factor <= 0.0:
            msg = f"scale factor must be positive, got {factor}"
            raise ValueError(msg)

        return Region(
            self.left * factor,
            self.top * factor,
            self.width * factor,
            self.height * factor,
        )


def _sample_normal_in_interval(
    origin: float,
    length: float,
    edge_sigma: float,
) -> float:
    """Samples a random value within interval using normal distribution.

    The distribution is centered at the midpoint of the interval, and
    the standard deviation is computed as (length / 2) / edge_sigma.
    Reject sampling ensures the result lies strictly
    within (origin, origin+length).

    Note:
        This function does not validate parameters.

    Args:
        origin: The starting coordinate of the interval
            (e.g., left or top).
        length: The size of the interval (e.g., width or height).
        edge_sigma: Controls spread; smaller values concentrate
            near center.

    Returns:
        A random value inside the interval.
    """
    end = origin + length
    mu = origin + length / 2.0
    sigma = (length / 2.0) / edge_sigma
    while True:
        p = random.normalvariate(mu, sigma)
        if origin < p < end:
            return p


def get_random_point_in_region(
    region: Region,
    edge_sigma: float = DEFAULT_EDGE_SIGMA,
) -> tuple[float, float]:
    """Returns random point in region.

    The point is sampled from a normal distribution centered at
    the region midpoint.

    Note:
        This function does not validate parameters.

    Args:
        region: Rectangular region defined by top-left corner and size.
        edge_sigma: Controls spread; smaller values concentrate
            near center. Defaults to 0.2.

    Returns:
        A random point (x, y) inside the region.
    """
    x = _sample_normal_in_interval(region.left, region.width, edge_sigma)
    y = _sample_normal_in_interval(region.top, region.height, edge_sigma)

    return (x, y)
