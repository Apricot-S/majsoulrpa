from dataclasses import dataclass

BASE_VIEWPORT_WIDTH = 1920
BASE_VIEWPORT_HEIGHT = 1080


@dataclass(frozen=True)
class Region:
    left: float
    top: float
    width: float
    height: float

    @property
    def right(self) -> float:
        return self.left + self.width

    @property
    def bottom(self) -> float:
        return self.top + self.height

    def scale_to_viewport(self, *, width: int, height: int) -> "Region":
        scale_x = width / BASE_VIEWPORT_WIDTH
        scale_y = height / BASE_VIEWPORT_HEIGHT
        if scale_x != scale_y:
            msg = "viewport aspect ratio must match 16:9."
            raise ValueError(msg)

        return Region(
            left=round(self.left * scale_x),
            top=round(self.top * scale_y),
            width=max(
                1,
                round(self.right * scale_x) - round(self.left * scale_x),
            ),
            height=max(
                1,
                round(self.bottom * scale_y) - round(self.top * scale_y),
            ),
        )
