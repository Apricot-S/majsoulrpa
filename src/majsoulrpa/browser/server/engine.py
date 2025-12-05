from dataclasses import dataclass
from pathlib import Path

from playwright.async_api import ViewportSize

from majsoulrpa.browser.server.config import Config
from majsoulrpa.constants import DEFAULT_VIEWPORT_HEIGHT
from majsoulrpa.exceptions import UserInputError


@dataclass(frozen=True)
class Option:
    user_data_dir: Path | None
    window_left: int
    window_top: int
    viewport_height: int
    headless: bool

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


def create_browser_args(config: Config, option: Option) -> list[str]:
    window_position = (
        f"--window-position={option.window_left},{option.window_top}"
    )
    proxy_server = f"--proxy-server=http://localhost:{config.proxy_port}"
    ignore_certificate_errors = "--ignore-certificate-errors"
    return [window_position, proxy_server, ignore_certificate_errors]


def create_ignored_default_args(option: Option) -> list[str]:
    return [] if option.headless else ["--mute-audio"]


def get_viewport_size(option: Option) -> tuple[ViewportSize, float]:
    height = option.viewport_height
    width = height * 16 // 9
    scale = height / DEFAULT_VIEWPORT_HEIGHT
    return ViewportSize(width=width, height=height), scale
