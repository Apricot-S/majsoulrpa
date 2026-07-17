from majsoulrpa.assets.templates.home import (
    EVENT_CLOSE_SETTINGS_PATH,
    EVENT_CLOSE_TEMPLATE_PATH,
    FRIENDLY_MATCH_SETTINGS_PATH,
    FRIENDLY_MATCH_TEMPLATE_PATH,
    JADE_SETTINGS_PATH,
    JADE_TEMPLATE_PATH,
    MAIL_CLOSE_SETTINGS_PATH,
    MAIL_CLOSE_TEMPLATE_PATH,
    NOTIFICATION_CLOSE_SETTINGS_PATH,
    NOTIFICATION_CLOSE_TEMPLATE_PATH,
    REWARDS_CONFIRM_SETTINGS_PATH,
    REWARDS_CONFIRM_TEMPLATE_PATH,
    REWARDS_SIGN_IN_SETTINGS_PATH,
    REWARDS_SIGN_IN_TEMPLATE_PATH,
    SUMMON_SETTINGS_PATH,
    SUMMON_TEMPLATE_PATH,
    TOURNAMENT_MATCH_SETTINGS_PATH,
    TOURNAMENT_MATCH_TEMPLATE_PATH,
)
from majsoulrpa.screens import (
    Screen,
    ScreenDetectionSpec,
)
from majsoulrpa.screens.errors import (
    ScreenInconsistentMessageError,
)
from majsoulrpa.screens.home import (
    HomeScreen,
)
from tests.screens.home._support import (
    _synthetic_blank_screenshot,
    _synthetic_template_screenshot,
)


def test_home_screen_is_screen() -> None:
    assert issubclass(HomeScreen, Screen)


def test_inconsistent_message_error_is_runtime_error() -> None:
    assert issubclass(ScreenInconsistentMessageError, RuntimeError)


def test_summon_template_assets_exist() -> None:
    assert SUMMON_TEMPLATE_PATH.name == "summon.png"
    assert SUMMON_TEMPLATE_PATH.is_file()
    assert SUMMON_SETTINGS_PATH.name == "summon.toml"
    assert SUMMON_SETTINGS_PATH.is_file()


def test_notification_close_template_assets_exist() -> None:
    assert NOTIFICATION_CLOSE_TEMPLATE_PATH.name == "notification-close.png"
    assert NOTIFICATION_CLOSE_TEMPLATE_PATH.is_file()
    assert NOTIFICATION_CLOSE_SETTINGS_PATH.name == "notification-close.toml"
    assert NOTIFICATION_CLOSE_SETTINGS_PATH.is_file()


def test_event_close_template_assets_exist() -> None:
    assert EVENT_CLOSE_TEMPLATE_PATH.name == "event-close.png"
    assert EVENT_CLOSE_TEMPLATE_PATH.is_file()
    assert EVENT_CLOSE_SETTINGS_PATH.name == "event-close.toml"
    assert EVENT_CLOSE_SETTINGS_PATH.is_file()


def test_mail_close_template_assets_exist() -> None:
    assert MAIL_CLOSE_TEMPLATE_PATH.name == "mail-close.png"
    assert MAIL_CLOSE_TEMPLATE_PATH.is_file()
    assert MAIL_CLOSE_SETTINGS_PATH.name == "mail-close.toml"
    assert MAIL_CLOSE_SETTINGS_PATH.is_file()


def test_rewards_template_assets_exist() -> None:
    assert REWARDS_SIGN_IN_TEMPLATE_PATH.name == "rewards-sign-in.png"
    assert REWARDS_SIGN_IN_TEMPLATE_PATH.is_file()
    assert REWARDS_SIGN_IN_SETTINGS_PATH.name == "rewards-sign-in.toml"
    assert REWARDS_SIGN_IN_SETTINGS_PATH.is_file()
    assert REWARDS_CONFIRM_TEMPLATE_PATH.name == "rewards-confirm.png"
    assert REWARDS_CONFIRM_TEMPLATE_PATH.is_file()
    assert REWARDS_CONFIRM_SETTINGS_PATH.name == "rewards-confirm.toml"
    assert REWARDS_CONFIRM_SETTINGS_PATH.is_file()


def test_jade_template_assets_exist() -> None:
    assert JADE_TEMPLATE_PATH.name == "jade.png"
    assert JADE_TEMPLATE_PATH.is_file()
    assert JADE_SETTINGS_PATH.name == "jade.toml"
    assert JADE_SETTINGS_PATH.is_file()


def test_match_button_template_assets_exist() -> None:
    assert TOURNAMENT_MATCH_TEMPLATE_PATH.name == "tournament-match.png"
    assert TOURNAMENT_MATCH_TEMPLATE_PATH.is_file()
    assert TOURNAMENT_MATCH_SETTINGS_PATH.name == "tournament-match.toml"
    assert TOURNAMENT_MATCH_SETTINGS_PATH.is_file()
    assert FRIENDLY_MATCH_TEMPLATE_PATH.name == "friendly-match.png"
    assert FRIENDLY_MATCH_TEMPLATE_PATH.is_file()
    assert FRIENDLY_MATCH_SETTINGS_PATH.name == "friendly-match.toml"
    assert FRIENDLY_MATCH_SETTINGS_PATH.is_file()


def test_home_screen_detection_spec_uses_summon_template() -> None:
    spec = HomeScreen.detection_spec()

    assert isinstance(spec, ScreenDetectionSpec)
    assert spec.matches(
        _synthetic_template_screenshot(
            template_path=SUMMON_TEMPLATE_PATH,
            settings_path=SUMMON_SETTINGS_PATH,
        ),
    )


def test_home_screen_does_not_match_blank_screenshot() -> None:
    assert not HomeScreen.detection_spec().matches(
        _synthetic_blank_screenshot(),
    )
