from dataclasses import dataclass
from math import isfinite
from random import Random

from majsoulrpa.constants import BASE_VIEWPORT_HEIGHT, BASE_VIEWPORT_WIDTH

# sqrt(-2.0 * log((4.0 - pi) / 4.0)) ~= 1.76
DEFAULT_BOUNDARY_SIGMA = 1.76
_DEFAULT_RANDOM = Random()  # noqa: S311


@dataclass(frozen=True)
class Region:
    left: float
    top: float
    width: float
    height: float

    def __post_init__(self) -> None:
        if not all(
            isfinite(value)
            for value in (self.left, self.top, self.width, self.height)
        ):
            msg = "region coordinates and size must be finite."
            raise ValueError(msg)
        if self.width <= 0 or self.height <= 0:
            msg = "region size must be positive."
            raise ValueError(msg)

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    def scale_to_viewport(self, *, width: int, height: int) -> "Region":
        if not isfinite(width) or not isfinite(height):
            msg = "viewport size must be finite."
            raise ValueError(msg)

        scale_x = width / BASE_VIEWPORT_WIDTH
        scale_y = height / BASE_VIEWPORT_HEIGHT
        if scale_x != scale_y:
            msg = "viewport aspect ratio must match 16:9."
            raise ValueError(msg)

        scaled_width = round(self.width * scale_x)
        scaled_height = round(self.height * scale_y)
        if scaled_width <= 0 or scaled_height <= 0:
            msg = "scaled region size must be positive."
            raise ValueError(msg)

        return Region(
            left=round(self.left * scale_x),
            top=round(self.top * scale_y),
            width=scaled_width,
            height=scaled_height,
        )

    def random_point(
        self,
        *,
        boundary_sigma: float = DEFAULT_BOUNDARY_SIGMA,
        rng: Random | None = None,
    ) -> tuple[float, float]:
        random_source = rng or _DEFAULT_RANDOM
        x = _sample_truncated_normal(
            self.left,
            self.width,
            boundary_sigma,
            random_source,
        )
        y = _sample_truncated_normal(
            self.top,
            self.height,
            boundary_sigma,
            random_source,
        )
        return (x, y)


# `boundary_sigma` specifies the distance from the center to each edge
# of the region, measured in standard deviations.
#
# Points are sampled independently for each axis from a normal
# distribution centered on the region, then rejected when they fall
# outside the region.
# Therefore, the resulting distribution is concentrated near the center
# and does not correspond to truncating a two-dimensional normal
# distribution by the inscribed ellipse.
#
# The default value is derived from the radius `r` for which an
# untruncated isotropic 2D standard normal distribution satisfies:
#
#     P(sqrt(x**2 + y**2) < r) = pi / 4
#
# where `pi / 4` is the area ratio of an ellipse inscribed in a
# rectangle.
# This is only a heuristic for selecting the default spread; it does not
# mean that pi / 4 of the generated points lie inside the inscribed
# ellipse.
def _sample_truncated_normal(
    origin: float,
    length: float,
    boundary_sigma: float,
    rng: Random,
) -> float:
    if not isfinite(boundary_sigma):
        msg = "boundary_sigma must be finite."
        raise ValueError(msg)
    if boundary_sigma <= 0:
        msg = "boundary_sigma must be positive."
        raise ValueError(msg)

    end = origin + length
    mu = origin + length / 2.0
    sigma = (length / 2.0) / boundary_sigma
    while True:
        p = rng.normalvariate(mu, sigma)
        if origin < p < end:
            return p
