import importlib
import sys
import tomllib
from pathlib import Path
from types import ModuleType

import pytest

import majsoulrpa


def test_package_exposes_string_version() -> None:
    assert isinstance(majsoulrpa.__version__, str)
    assert majsoulrpa.__version__


def test_public_exports_are_explicit() -> None:
    assert majsoulrpa.__all__ == ["AppConfig", "RPAApp", "__version__"]


def test_optional_dependency_extra_names_are_defined() -> None:
    pyproject = tomllib.loads(
        Path("pyproject.toml").read_text(encoding="utf-8"),
    )

    assert set(pyproject["project"]["optional-dependencies"]) == {
        "browser",
        "rpa",
        "s3",
    }


def test_presentation_import_does_not_load_opencv_template_module() -> None:
    sys.modules.pop("majsoulrpa.presentation", None)
    sys.modules.pop("majsoulrpa.presentation.template", None)
    if hasattr(majsoulrpa, "presentation"):
        delattr(majsoulrpa, "presentation")

    importlib.import_module("majsoulrpa.presentation")

    assert "majsoulrpa.presentation.template" not in sys.modules


def test_browser_import_does_not_load_playwright_backend_module() -> None:
    sys.modules.pop("majsoulrpa.browser", None)
    sys.modules.pop("majsoulrpa.browser.playwright", None)
    if hasattr(majsoulrpa, "browser"):
        delattr(majsoulrpa, "browser")

    importlib.import_module("majsoulrpa.browser")

    assert "majsoulrpa.browser.playwright" not in sys.modules


def test_screens_import_does_not_load_concrete_screen_modules() -> None:
    sys.modules.pop("majsoulrpa.screens", None)
    sys.modules.pop("majsoulrpa.screens.login", None)
    sys.modules.pop("majsoulrpa.screens.room", None)
    if hasattr(majsoulrpa, "screens"):
        delattr(majsoulrpa, "screens")

    screens = importlib.import_module("majsoulrpa.screens")

    assert screens.__all__ == [
        "Screen",
        "ScreenContext",
        "ScreenDetectionError",
        "ScreenDetectionSpec",
        "ScreenDetectionTimeoutError",
        "ScreenError",
        "ScreenInconsistentMessageError",
        "ScreenInvalidArgumentError",
        "ScreenInvalidOperationError",
        "ScreenNotImplementedOperationError",
        "ScreenStaleError",
        "ScreenUnexpectedStateError",
    ]
    assert "majsoulrpa.screens.login" not in sys.modules
    assert "majsoulrpa.screens.room" not in sys.modules


def test_room_import_does_not_load_opencv_template_module() -> None:
    sys.modules.pop("majsoulrpa.screens.room", None)
    sys.modules.pop("majsoulrpa.screens.room.screen", None)
    sys.modules.pop("majsoulrpa.presentation.template", None)

    room = importlib.import_module("majsoulrpa.screens.room")

    assert room.__all__ == [
        "RoomOperation",
        "RoomOperationFailureReason",
        "RoomOperationNotAllowedError",
        "RoomOperationNotAllowedReason",
        "RoomOperationRejectedError",
        "RoomPlayer",
        "RoomScreen",
        "RoomState",
        "RoomStatus",
    ]
    assert "majsoulrpa.screens.room.screen" not in sys.modules
    assert "majsoulrpa.presentation.template" not in sys.modules


def test_room_screen_attribute_loads_opencv_template_module() -> None:
    sys.modules.pop("majsoulrpa.screens.room", None)
    sys.modules.pop("majsoulrpa.screens.room.screen", None)
    sys.modules.pop("majsoulrpa.presentation.template", None)

    room = importlib.import_module("majsoulrpa.screens.room")

    assert room.RoomScreen.__name__ == "RoomScreen"
    assert "majsoulrpa.screens.room.screen" in sys.modules
    assert "majsoulrpa.presentation.template" in sys.modules


def test_browser_public_exports_are_minimal() -> None:
    browser = importlib.import_module("majsoulrpa.browser")

    assert browser.__all__ == [
        "BrowserOperationError",
        "PlaywrightBrowserBackend",
        "PlaywrightCommandExecutor",
        "run_browser_host",
    ]


def test_presentation_lazy_exports_are_cached_and_listed() -> None:
    sys.modules.pop("majsoulrpa.presentation", None)
    if hasattr(majsoulrpa, "presentation"):
        delattr(majsoulrpa, "presentation")
    presentation = importlib.import_module("majsoulrpa.presentation")

    assert "TemplateMatcher" in dir(presentation)
    assert "TemplateMatcher" not in presentation.__dict__

    value = presentation.TemplateMatcher

    assert presentation.__dict__["TemplateMatcher"] is value


def test_browser_lazy_exports_are_cached_and_listed() -> None:
    sys.modules.pop("majsoulrpa.browser", None)
    if hasattr(majsoulrpa, "browser"):
        delattr(majsoulrpa, "browser")
    browser = importlib.import_module("majsoulrpa.browser")

    assert "PlaywrightBrowserBackend" in dir(browser)
    assert "PlaywrightBrowserBackend" not in browser.__dict__

    value = browser.PlaywrightBrowserBackend

    assert browser.__dict__["PlaywrightBrowserBackend"] is value


def test_presentation_lazy_export_reports_missing_rpa_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sys.modules.pop("majsoulrpa.presentation", None)
    if hasattr(majsoulrpa, "presentation"):
        delattr(majsoulrpa, "presentation")
    presentation = importlib.import_module("majsoulrpa.presentation")

    def import_module(name: str) -> ModuleType:
        if name == "majsoulrpa.presentation.template":
            msg = "No module named 'cv2'"
            raise ModuleNotFoundError(msg, name="cv2")
        return importlib.import_module(name)

    monkeypatch.setattr(presentation.importlib, "import_module", import_module)

    with pytest.raises(ModuleNotFoundError, match=r"majsoulrpa\[rpa\]"):
        _ = presentation.TemplateMatcher


def test_presentation_lazy_export_preserves_unrelated_import_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sys.modules.pop("majsoulrpa.presentation", None)
    if hasattr(majsoulrpa, "presentation"):
        delattr(majsoulrpa, "presentation")
    presentation = importlib.import_module("majsoulrpa.presentation")

    def import_module(name: str) -> ModuleType:
        if name == "majsoulrpa.presentation.template":
            missing_name = "template_transitive_dependency"
            msg = f"No module named {missing_name!r}"
            raise ModuleNotFoundError(msg, name=missing_name)
        return importlib.import_module(name)

    monkeypatch.setattr(presentation.importlib, "import_module", import_module)

    with pytest.raises(
        ModuleNotFoundError,
        match="template_transitive_dependency",
    ) as exc_info:
        _ = presentation.TemplateMatcher

    assert exc_info.value.name == "template_transitive_dependency"


def test_browser_lazy_export_reports_missing_browser_extra(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sys.modules.pop("majsoulrpa.browser", None)
    if hasattr(majsoulrpa, "browser"):
        delattr(majsoulrpa, "browser")
    browser = importlib.import_module("majsoulrpa.browser")

    def import_module(name: str) -> ModuleType:
        if name == "majsoulrpa.browser.playwright":
            msg = "No module named 'playwright'"
            raise ModuleNotFoundError(msg, name="playwright")
        return importlib.import_module(name)

    monkeypatch.setattr(browser.importlib, "import_module", import_module)

    with pytest.raises(ModuleNotFoundError, match=r"majsoulrpa\[browser\]"):
        _ = browser.PlaywrightBrowserBackend


def test_browser_lazy_export_preserves_unrelated_import_failure(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sys.modules.pop("majsoulrpa.browser", None)
    if hasattr(majsoulrpa, "browser"):
        delattr(majsoulrpa, "browser")
    browser = importlib.import_module("majsoulrpa.browser")

    def import_module(name: str) -> ModuleType:
        if name == "majsoulrpa.browser.playwright":
            missing_name = "browser_transitive_dependency"
            msg = f"No module named {missing_name!r}"
            raise ModuleNotFoundError(msg, name=missing_name)
        return importlib.import_module(name)

    monkeypatch.setattr(browser.importlib, "import_module", import_module)

    with pytest.raises(
        ModuleNotFoundError,
        match="browser_transitive_dependency",
    ) as exc_info:
        _ = browser.PlaywrightBrowserBackend

    assert exc_info.value.name == "browser_transitive_dependency"
