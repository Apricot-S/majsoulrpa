from majsoulrpa.assets import TEMPLATES_DIR

ROOM_SIGN_SETTINGS_PATH = TEMPLATES_DIR / "room" / "room-sign.toml"
ROOM_SIGN_TEMPLATE_PATH = TEMPLATES_DIR / "room" / "room-sign.png"

LEAVE_SETTINGS_PATH = TEMPLATES_DIR / "room" / "leave.toml"
LEAVE_TEMPLATE_PATH = TEMPLATES_DIR / "room" / "leave.png"
ADD_AI_SETTINGS_PATHS = tuple(
    TEMPLATES_DIR / "room" / f"add-ai-{index}.toml" for index in range(4)
)
ADD_AI_TEMPLATE_PATH = TEMPLATES_DIR / "room" / "add-ai.png"

__all__ = [
    "ADD_AI_SETTINGS_PATHS",
    "ADD_AI_TEMPLATE_PATH",
    "LEAVE_SETTINGS_PATH",
    "LEAVE_TEMPLATE_PATH",
    "ROOM_SIGN_SETTINGS_PATH",
    "ROOM_SIGN_TEMPLATE_PATH",
]
