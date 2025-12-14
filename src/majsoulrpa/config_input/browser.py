from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa import constants
from majsoulrpa.config_input._common import _to_kebab


class Browser(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=_to_kebab)

    window_left: int = Field(0)
    window_top: int = Field(0)
    viewport_height: int = Field(constants.DEFAULT_VIEWPORT_HEIGHT)
    headless: bool = Field(default=False)
    user_data_dir: Path | None = Field(None)
