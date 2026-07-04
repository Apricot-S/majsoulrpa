from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field

USER_PORT_MIN = 1024
USER_PORT_MAX = 49151
UserPort = Annotated[int, Field(ge=USER_PORT_MIN, le=USER_PORT_MAX)]

Host = Annotated[str, Field(min_length=1)]
ViewportHeight = Literal[720, 1080, 1440]


class EndpointConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    browser_host: Host = "127.0.0.1"
    client_host: Host = "127.0.0.1"
    remote_port: UserPort = 19222
    sniffer_port: UserPort = 37247


class BrowserConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    window_left: int = 0
    window_top: int = 0
    viewport_height: ViewportHeight = 1080
    headless: bool = False
    user_data_dir: Path | None = None


class AppConfig(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    endpoint: EndpointConfig = Field(default_factory=EndpointConfig)
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
