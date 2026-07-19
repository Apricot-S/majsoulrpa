from majsoulrpa.assets.templates.room import (
    ROOM_SIGN_SETTINGS_PATH,
    ROOM_SIGN_TEMPLATE_PATH,
)
from majsoulrpa.screens import Screen, ScreenDetectionSpec
from majsoulrpa.screens.room import RoomScreen
from tests.screens._support import (
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)


def test_room_sign_template_assets_exist() -> None:
    assert ROOM_SIGN_TEMPLATE_PATH.name == "room-sign.png"
    assert ROOM_SIGN_TEMPLATE_PATH.is_file()
    assert ROOM_SIGN_SETTINGS_PATH.name == "room-sign.toml"
    assert ROOM_SIGN_SETTINGS_PATH.is_file()


def test_room_screen_is_screen() -> None:
    assert issubclass(RoomScreen, Screen)


def test_room_screen_detection_spec_uses_room_sign_template() -> None:
    spec = RoomScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)
    assert spec.matches(
        _synthetic_template_screenshot(
            template_path=ROOM_SIGN_TEMPLATE_PATH,
            settings_path=ROOM_SIGN_SETTINGS_PATH,
        ),
    )


def test_room_screen_does_not_match_blank_screenshot() -> None:
    assert not RoomScreen.detection_spec().matches(
        _synthetic_blank_screenshot(),
    )
