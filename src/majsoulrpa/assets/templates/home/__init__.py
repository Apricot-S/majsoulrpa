from majsoulrpa.assets import TEMPLATES_DIR

SUMMON_SETTINGS_PATH = TEMPLATES_DIR / "home" / "summon.toml"
SUMMON_TEMPLATE_PATH = TEMPLATES_DIR / "home" / "summon.png"

NOTIFICATION_CLOSE_SETTINGS_PATH = (
    TEMPLATES_DIR / "home" / "notification-close.toml"
)
NOTIFICATION_CLOSE_TEMPLATE_PATH = (
    TEMPLATES_DIR / "home" / "notification-close.png"
)

__all__ = [
    "NOTIFICATION_CLOSE_SETTINGS_PATH",
    "NOTIFICATION_CLOSE_TEMPLATE_PATH",
    "SUMMON_SETTINGS_PATH",
    "SUMMON_TEMPLATE_PATH",
]
