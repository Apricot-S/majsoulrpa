import tomllib
from pathlib import Path
from typing import Annotated, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    model_validator,
)

from majsoulrpa.constants import (
    DEFAULT_BROWSER_HOST,
    DEFAULT_CLIENT_HOST,
    DEFAULT_REMOTE_PORT,
    DEFAULT_SNIFFER_PORT,
    DEFAULT_VIEWPORT_HEIGHT,
    DEFAULT_WINDOW_LEFT,
    DEFAULT_WINDOW_TOP,
    SUPPORTED_VIEWPORT_HEIGHTS,
    USER_PORT_MAX,
    USER_PORT_MIN,
)


def _validate_host(value: str) -> str:
    if any(character.isspace() for character in value):
        msg = "host must not contain whitespace."
        raise ValueError(msg)
    return value


Host = Annotated[
    str,
    Field(min_length=1),
    AfterValidator(_validate_host),
]
UserPort = Annotated[int, Field(ge=USER_PORT_MIN, le=USER_PORT_MAX)]


def _validate_viewport_height(value: int) -> int:
    if value not in SUPPORTED_VIEWPORT_HEIGHTS:
        msg = "viewport_height must be one of supported viewport heights."
        raise ValueError(msg)
    return value


ViewportHeight = Annotated[int, AfterValidator(_validate_viewport_height)]


class _ConfigModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        hide_input_in_errors=True,
    )


class EndpointConfig(_ConfigModel):
    browser_host: Host = DEFAULT_BROWSER_HOST
    client_host: Host = DEFAULT_CLIENT_HOST
    remote_port: UserPort = DEFAULT_REMOTE_PORT
    sniffer_port: UserPort = DEFAULT_SNIFFER_PORT

    @model_validator(mode="after")
    def _validate_distinct_ports(self) -> Self:
        if self.remote_port == self.sniffer_port:
            msg = "remote_port and sniffer_port must be different."
            raise ValueError(msg)
        return self


class BrowserConfig(_ConfigModel):
    window_left: int = DEFAULT_WINDOW_LEFT
    window_top: int = DEFAULT_WINDOW_TOP
    viewport_height: ViewportHeight = DEFAULT_VIEWPORT_HEIGHT
    headless: bool = False
    user_data_dir: Annotated[Path, Field(strict=False)] | None = None


class YostarEmailS3Config(_ConfigModel):
    bucket_name: Annotated[str, Field(min_length=1)]
    key_prefix: str = ""
    aws_profile: Annotated[str, Field(min_length=1)] | None = None


class YostarEmailConfig(_ConfigModel):
    email_address: Annotated[str, Field(min_length=1, repr=False)]
    s3: YostarEmailS3Config | None = None


class AppConfig(_ConfigModel):
    endpoint: EndpointConfig = Field(default_factory=EndpointConfig)
    browser: BrowserConfig = Field(default_factory=BrowserConfig)
    yostar_email: YostarEmailConfig | None = None

    @classmethod
    def from_toml_text(cls, text: str) -> Self:
        return cls.model_validate(tomllib.loads(text))

    @classmethod
    def from_toml_file(cls, path: Path) -> Self:
        with path.open("rb") as fp:
            return cls.model_validate(tomllib.load(fp))
