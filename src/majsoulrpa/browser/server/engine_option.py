from dataclasses import dataclass
from pathlib import Path

from majsoulrpa.exceptions import UserInputError

MAJSOUL_URL = "https://game.mahjongsoul.com/"  # JP version


@dataclass(frozen=True)
class Option:
    user_data_dir: Path | None
    window_left: int
    window_top: int
    viewport_height: int
    headless: bool
    url: str = MAJSOUL_URL

    def __post_init__(self) -> None:
        if self.user_data_dir is not None:
            resolved = resolve_user_data_dir(self.user_data_dir)
            object.__setattr__(self, "user_data_dir", resolved)

        validate_viewport_height(self.viewport_height)


def resolve_user_data_dir(path: Path) -> Path:
    p = path.resolve(strict=False)
    if p.exists() and p.is_file():
        msg = "invalid user-data-dir: file exists"
        raise UserInputError(msg)
    return p


def validate_viewport_height(h: int) -> None:
    if h <= 0:
        msg = f"viewport-height must be positive: {h}"
        raise UserInputError(msg)

    if h % 9 != 0:
        msg = f"viewport-height is not a valid 16:9 resolution: {h}"
        raise UserInputError(msg)

    w = h * 16 // 9
    if w * 9 != h * 16:
        msg = f"viewport-height is not a valid 16:9 resolution: {h}"
        raise UserInputError(msg)
