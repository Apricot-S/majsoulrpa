from majsoulrpa.assets.templates.home import (
    FRIENDLY_MATCH_SETTINGS_PATH,
    FRIENDLY_MATCH_TEMPLATE_PATH,
    TOURNAMENT_MATCH_SETTINGS_PATH,
    TOURNAMENT_MATCH_TEMPLATE_PATH,
)
from tests.screens._support import _synthetic_templates_screenshot


def _synthetic_home_ready_screenshot() -> bytes:
    return _synthetic_templates_screenshot(
        (
            (
                TOURNAMENT_MATCH_TEMPLATE_PATH,
                TOURNAMENT_MATCH_SETTINGS_PATH,
            ),
            (FRIENDLY_MATCH_TEMPLATE_PATH, FRIENDLY_MATCH_SETTINGS_PATH),
        ),
    )
