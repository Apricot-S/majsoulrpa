from pathlib import Path

import pytest
from playwright.async_api import ViewportSize

from majsoulrpa.browser.server.engine import (
    Option,
    create_browser_args,
    create_ignored_default_args,
    get_viewport_size,
)
from majsoulrpa.exceptions import UserInputError

from .test_config import make_config


def make_option(
    *,
    user_data_dir: Path | None = None,
    window_left: int = 0,
    window_top: int = 0,
    viewport_height: int = 1080,
    headless: bool = False,
) -> Option:
    return Option(
        user_data_dir=user_data_dir,
        window_left=window_left,
        window_top=window_top,
        viewport_height=viewport_height,
        headless=headless,
    )


def test_option_none_user_data_dir() -> None:
    opt = make_option(user_data_dir=None)
    assert opt.user_data_dir is None


def test_option_existing_dir(tmp_path: Path) -> None:
    opt = make_option(user_data_dir=tmp_path)
    assert opt.user_data_dir == tmp_path.resolve()


def test_option_existing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "file"
    file_path.write_text("dummy")
    with pytest.raises(UserInputError):
        make_option(user_data_dir=file_path)


def test_option_nonexistent_dir(tmp_path: Path) -> None:
    nonexistent = tmp_path / "does_not_exist"
    opt = make_option(user_data_dir=nonexistent)
    assert opt.user_data_dir == nonexistent.resolve()
    assert not nonexistent.exists()


@pytest.mark.parametrize(
    ("window_left", "window_top"),
    [(0, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)],
)
def test_option_window_position(window_left: int, window_top: int) -> None:
    opt = make_option(window_left=window_left, window_top=window_top)
    assert opt.window_left == window_left
    assert opt.window_top == window_top


@pytest.mark.parametrize("viewport_height", [540, 720, 900, 1080, 1440, 2160])
def test_option_16_9_viewport_height(viewport_height: int) -> None:
    opt = make_option(viewport_height=viewport_height)
    assert opt.viewport_height == viewport_height


@pytest.mark.parametrize("viewport_height", [-1080, 0, 768])
def test_option_invalid_viewport_height(viewport_height: int) -> None:
    with pytest.raises(UserInputError):
        make_option(viewport_height=viewport_height)


@pytest.mark.parametrize(
    ("window_left", "window_top", "expected"),
    [
        (
            0,
            0,
            [
                "--window-position=0,0",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            100,
            0,
            [
                "--window-position=100,0",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            0,
            -50,
            [
                "--window-position=0,-50",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            -200,
            100,
            [
                "--window-position=-200,100",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
    ],
)
def test_create_browser_args_window_position(
    window_left: int,
    window_top: int,
    expected: list[str],
) -> None:
    cfg = make_config()
    opt = make_option(window_left=window_left, window_top=window_top)
    assert create_browser_args(cfg, opt) == expected


@pytest.mark.parametrize(
    ("proxy_port", "expected"),
    [
        (
            8080,
            [
                "--window-position=0,0",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            8081,
            [
                "--window-position=0,0",
                "--proxy-server=http://localhost:8081",
                "--ignore-certificate-errors",
            ],
        ),
    ],
)
def test_create_browser_args_proxy_server(
    proxy_port: int,
    expected: list[str],
) -> None:
    cfg = make_config(proxy_port=proxy_port)
    opt = make_option()
    assert create_browser_args(cfg, opt) == expected


@pytest.mark.parametrize(
    ("headless", "expected"),
    [(True, []), (False, ["--mute-audio"])],
)
def test_create_ignored_default_args(
    headless: bool,  # noqa: FBT001
    expected: list[str],
) -> None:
    opt = make_option(headless=headless)
    assert create_ignored_default_args(opt) == expected


@pytest.mark.parametrize(
    ("viewport_height", "expected"),
    [
        (1080, (ViewportSize(width=1920, height=1080), 1.0)),
        (540, (ViewportSize(width=960, height=540), 0.5)),
        (720, (ViewportSize(width=1280, height=720), 2 / 3)),
        (900, (ViewportSize(width=1600, height=900), 5 / 6)),
        (1440, (ViewportSize(width=2560, height=1440), 4 / 3)),
    ],
)
def test_get_viewport_size(
    viewport_height: int,
    expected: tuple[ViewportSize, float],
) -> None:
    opt = make_option(viewport_height=viewport_height)
    assert get_viewport_size(opt) == expected
