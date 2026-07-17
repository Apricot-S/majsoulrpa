from majsoulrpa.assets import TEMPLATES_DIR

CONFIRM_SETTINGS_PATH = TEMPLATES_DIR / "home" / "join_room" / "confirm.toml"
CONFIRM_TEMPLATE_PATH = TEMPLATES_DIR / "home" / "join_room" / "confirm.png"
ERROR_CONFIRM_SETTINGS_PATH = (
    TEMPLATES_DIR / "home" / "join_room" / "error-confirm.toml"
)
ERROR_CONFIRM_TEMPLATE_PATH = (
    TEMPLATES_DIR / "home" / "join_room" / "error-confirm.png"
)

__all__ = [
    "CONFIRM_SETTINGS_PATH",
    "CONFIRM_TEMPLATE_PATH",
    "ERROR_CONFIRM_SETTINGS_PATH",
    "ERROR_CONFIRM_TEMPLATE_PATH",
]
