from pathlib import Path

from pydantic import BaseModel, ConfigDict

from majsoulrpa import constants
from majsoulrpa.config_input._common import _to_kebab


class Browser(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        alias_generator=_to_kebab,
        serialize_by_alias=True,
    )

    window_left: int = 0
    window_top: int = 0
    viewport_height: int = constants.DEFAULT_VIEWPORT_HEIGHT
    headless: bool = False
    user_data_dir: Path | None = None
