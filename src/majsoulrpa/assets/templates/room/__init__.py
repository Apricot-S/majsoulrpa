from majsoulrpa.assets import TEMPLATES_DIR

ROOM_SIGN_SETTINGS_PATH = TEMPLATES_DIR / "room" / "room-sign.toml"
ROOM_SIGN_TEMPLATE_PATH = TEMPLATES_DIR / "room" / "room-sign.png"

LEAVE_SETTINGS_PATH = TEMPLATES_DIR / "room" / "leave.toml"
LEAVE_TEMPLATE_PATH = TEMPLATES_DIR / "room" / "leave.png"

__all__ = [
    "LEAVE_SETTINGS_PATH",
    "LEAVE_TEMPLATE_PATH",
    "ROOM_SIGN_SETTINGS_PATH",
    "ROOM_SIGN_TEMPLATE_PATH",
]
