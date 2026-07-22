from majsoulrpa.assets import TEMPLATES_DIR

SEAT_INDICATOR_SETTINGS_PATH = TEMPLATES_DIR / "match" / "seat-indicator.toml"
SEAT_INDICATOR_TEMPLATE_PATHS = tuple(
    TEMPLATES_DIR / "match" / f"seat-indicator-{index}.png"
    for index in range(4)
)

BUTTON_AREA_SETTINGS_PATH = TEMPLATES_DIR / "match" / "button-area.toml"
CHI_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "chi.png"
PENG_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "peng.png"
LIQI_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "liqi.png"

__all__ = [
    "BUTTON_AREA_SETTINGS_PATH",
    "CHI_TEMPLATE_PATH",
    "LIQI_TEMPLATE_PATH",
    "PENG_TEMPLATE_PATH",
    "SEAT_INDICATOR_SETTINGS_PATH",
    "SEAT_INDICATOR_TEMPLATE_PATHS",
]
