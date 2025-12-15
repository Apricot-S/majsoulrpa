from pathlib import Path

import pytest
from pydantic import ValidationError

from majsoulrpa import constants
from majsoulrpa.config_input.browser import Browser


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("window_left", 0),
        ("window_top", 0),
        ("viewport_height", constants.DEFAULT_VIEWPORT_HEIGHT),
        ("headless", False),
        ("user_data_dir", None),
    ],
)
def test_defaults(field: str, expected: object) -> None:
    browser = Browser()
    assert getattr(browser, field) == expected


@pytest.mark.parametrize("window_left", [0, 100, -50])
def test_window_left_from_dict(window_left: int) -> None:
    browser = Browser.model_validate({"window-left": window_left})
    assert browser.window_left == window_left


@pytest.mark.parametrize("window_top", [0, 100, -50])
def test_window_top_from_dict(window_top: int) -> None:
    browser = Browser.model_validate({"window-top": window_top})
    assert browser.window_top == window_top


@pytest.mark.parametrize("viewport_height", [720, 0, -1080, 10])
def test_viewport_height_from_dict(viewport_height: int) -> None:
    browser = Browser.model_validate({"viewport-height": viewport_height})
    assert browser.viewport_height == viewport_height


@pytest.mark.parametrize("headless", [True, False, 0, 1])
def test_headless_from_dict(headless: object) -> None:
    browser = Browser.model_validate({"headless": headless})
    assert browser.headless == headless


@pytest.mark.parametrize(
    ("user_data_dir", "expected"),
    [
        (None, None),
        ("", Path()),
        (".", Path()),
        ("./user-data", Path("./user-data")),
    ],
)
def test_user_data_dir_from_dict(
    user_data_dir: Path | None,
    expected: Path | None,
) -> None:
    browser = Browser.model_validate({"user-data-dir": user_data_dir})
    assert browser.user_data_dir == expected


def test_allow_snake_case_key() -> None:
    browser = Browser.model_validate({"window_left": 1000})
    assert browser.window_left == 1000


def test_allow_arg() -> None:
    browser = Browser(window_top=100)
    assert browser.window_top == 100


def test_window_left_type_error() -> None:
    with pytest.raises(ValidationError):
        Browser.model_validate({"window-left": "not-an-int"})
