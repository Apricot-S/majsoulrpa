from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

PositiveDelay = Annotated[float, Field(gt=0)]


class ClickCommand(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["click"] = "click"
    x: float
    y: float
    mouse_down_up_delay_seconds: PositiveDelay


class TextInputCommand(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["text_input"] = "text_input"
    text: str
    character_delay_seconds: PositiveDelay


class ScreenshotCommand(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["screenshot"] = "screenshot"


BrowserCommand = Annotated[
    ClickCommand | TextInputCommand | ScreenshotCommand,
    Field(discriminator="type"),
]


class ClickResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["click"] = "click"
    x: float
    y: float


class TextInputResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["text_input"] = "text_input"
    text: str


class ScreenshotResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["screenshot"] = "screenshot"
    screenshot_base64: str


class BrowserErrorResponse(BaseModel):
    model_config = ConfigDict(extra="forbid", frozen=True)

    type: Literal["error"] = "error"
    message: str


BrowserResponse = Annotated[
    ClickResponse
    | TextInputResponse
    | ScreenshotResponse
    | BrowserErrorResponse,
    Field(discriminator="type"),
]

_BROWSER_COMMAND_ADAPTER = TypeAdapter(BrowserCommand)
_BROWSER_RESPONSE_ADAPTER = TypeAdapter(BrowserResponse)


def dump_browser_command_json(command: BrowserCommand) -> bytes:
    return _BROWSER_COMMAND_ADAPTER.dump_json(command)


def dump_browser_response_json(response: BrowserResponse) -> bytes:
    return _BROWSER_RESPONSE_ADAPTER.dump_json(response)


def parse_browser_command_json(payload: str | bytes) -> BrowserCommand:
    return _BROWSER_COMMAND_ADAPTER.validate_json(payload)


def parse_browser_response_json(payload: str | bytes) -> BrowserResponse:
    return _BROWSER_RESPONSE_ADAPTER.validate_json(payload)
