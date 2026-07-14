from majsoulrpa.assets import TEMPLATES_DIR

TOURNAMENT_ENTER_SETTINGS_PATH = (
    TEMPLATES_DIR / "home" / "tournament_lobby" / "enter.toml"
)
TOURNAMENT_ENTER_TEMPLATE_PATH = (
    TEMPLATES_DIR / "home" / "tournament_lobby" / "enter.png"
)
TOURNAMENT_CONFIRM_SETTINGS_PATH = (
    TEMPLATES_DIR / "home" / "tournament_lobby" / "confirm.toml"
)
TOURNAMENT_CONFIRM_TEMPLATE_PATH = (
    TEMPLATES_DIR / "home" / "tournament_lobby" / "confirm.png"
)

__all__ = [
    "TOURNAMENT_CONFIRM_SETTINGS_PATH",
    "TOURNAMENT_CONFIRM_TEMPLATE_PATH",
    "TOURNAMENT_ENTER_SETTINGS_PATH",
    "TOURNAMENT_ENTER_TEMPLATE_PATH",
]
