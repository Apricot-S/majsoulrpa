from majsoulrpa.assets import TEMPLATES_DIR

SEAT_INDICATOR_SETTINGS_PATH = TEMPLATES_DIR / "match" / "seat-indicator.toml"
SEAT_INDICATOR_TEMPLATE_PATHS = tuple(
    TEMPLATES_DIR / "match" / f"seat-indicator-{index}.png"
    for index in range(4)
)

BUTTON_AREA_SETTINGS_PATH = TEMPLATES_DIR / "match" / "button-area.toml"
CHI_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "chi.png"
PENG_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "peng.png"
GANG_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "gang.png"
LIQI_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "liqi.png"
BABEI_TEMPLATE_PATH = TEMPLATES_DIR / "match" / "babei.png"

__all__ = [
    "BABEI_TEMPLATE_PATH",
    "BUTTON_AREA_SETTINGS_PATH",
    "CHI_TEMPLATE_PATH",
    "GANG_TEMPLATE_PATH",
    "LIQI_TEMPLATE_PATH",
    "PENG_TEMPLATE_PATH",
    "SEAT_INDICATOR_SETTINGS_PATH",
    "SEAT_INDICATOR_TEMPLATE_PATHS",
]
