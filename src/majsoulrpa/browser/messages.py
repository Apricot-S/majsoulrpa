from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter

PositiveDelay = Annotated[float, Field(gt=0)]
NonEmptyKey = Annotated[str, Field(min_length=1)]
NonEmptyUrl = Annotated[str, Field(min_length=1)]


class _BrowserWireModel(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        strict=True,
        allow_inf_nan=False,
        hide_input_in_errors=True,
    )


class ClickCommand(_BrowserWireModel):
    type: Literal["click"] = "click"
    x: float
    y: float
    hover_delay_seconds: PositiveDelay | None
    mouse_down_up_delay_seconds: PositiveDelay


class MoveMouseCommand(_BrowserWireModel):
    type: Literal["move_mouse"] = "move_mouse"
    x: float
    y: float


class TextInputCommand(_BrowserWireModel):
    type: Literal["text_input"] = "text_input"
    text: str
    character_delay_seconds: PositiveDelay


class PressKeyCommand(_BrowserWireModel):
    type: Literal["press_key"] = "press_key"
    key: NonEmptyKey
    key_down_up_delay_seconds: PositiveDelay


class ScreenshotCommand(_BrowserWireModel):
    type: Literal["screenshot"] = "screenshot"


class GotoUrlCommand(_BrowserWireModel):
    type: Literal["goto_url"] = "goto_url"
    url: NonEmptyUrl


class ReloadCommand(_BrowserWireModel):
    type: Literal["reload"] = "reload"


class StopBrowserHostCommand(_BrowserWireModel):
    type: Literal["stop_browser_host"] = "stop_browser_host"


class ClickAndWaitForYostarAuthCommand(_BrowserWireModel):
    type: Literal["click_and_wait_for_yostar_auth"] = (
        "click_and_wait_for_yostar_auth"
    )
    x: float
    y: float
    mouse_down_up_delay_seconds: PositiveDelay
    timeout_seconds: PositiveDelay


BrowserCommand = Annotated[
    ClickCommand
    | MoveMouseCommand
    | TextInputCommand
    | PressKeyCommand
    | ScreenshotCommand
    | GotoUrlCommand
    | ReloadCommand
    | StopBrowserHostCommand
    | ClickAndWaitForYostarAuthCommand,
    Field(discriminator="type"),
]


class ClickResponse(_BrowserWireModel):
    type: Literal["click"] = "click"
    x: float
    y: float


class MoveMouseResponse(_BrowserWireModel):
    type: Literal["move_mouse"] = "move_mouse"
    x: float
    y: float


class TextInputResponse(_BrowserWireModel):
    type: Literal["text_input"] = "text_input"
    text: str


class PressKeyResponse(_BrowserWireModel):
    type: Literal["press_key"] = "press_key"
    key: str


class ScreenshotResponse(_BrowserWireModel):
    type: Literal["screenshot"] = "screenshot"
    screenshot_base64: str


class GotoUrlResponse(_BrowserWireModel):
    type: Literal["goto_url"] = "goto_url"
    url: str


class ReloadResponse(_BrowserWireModel):
    type: Literal["reload"] = "reload"


class StopBrowserHostResponse(_BrowserWireModel):
    type: Literal["stop_browser_host"] = "stop_browser_host"


class YostarAuthAcceptedResponse(_BrowserWireModel):
    type: Literal["yostar_auth_accepted"] = "yostar_auth_accepted"


class YostarAuthRejectedResponse(_BrowserWireModel):
    type: Literal["yostar_auth_rejected"] = "yostar_auth_rejected"
    application_code: int


class BrowserErrorResponse(_BrowserWireModel):
    type: Literal["error"] = "error"
    message: str


BrowserResponse = Annotated[
    ClickResponse
    | MoveMouseResponse
    | TextInputResponse
    | PressKeyResponse
    | ScreenshotResponse
    | GotoUrlResponse
    | ReloadResponse
    | StopBrowserHostResponse
    | YostarAuthAcceptedResponse
    | YostarAuthRejectedResponse
    | BrowserErrorResponse,
    Field(discriminator="type"),
]

_WIRE_ADAPTER_CONFIG = ConfigDict(hide_input_in_errors=True)
_BROWSER_COMMAND_ADAPTER = TypeAdapter(
    BrowserCommand,
    config=_WIRE_ADAPTER_CONFIG,
)
_BROWSER_RESPONSE_ADAPTER = TypeAdapter(
    BrowserResponse,
    config=_WIRE_ADAPTER_CONFIG,
)


def dump_browser_command_json(command: BrowserCommand) -> bytes:
    return _BROWSER_COMMAND_ADAPTER.dump_json(command)


def dump_browser_response_json(response: BrowserResponse) -> bytes:
    return _BROWSER_RESPONSE_ADAPTER.dump_json(response)


def parse_browser_command_json(payload: str | bytes) -> BrowserCommand:
    return _BROWSER_COMMAND_ADAPTER.validate_json(payload)


def parse_browser_response_json(payload: str | bytes) -> BrowserResponse:
    return _BROWSER_RESPONSE_ADAPTER.validate_json(payload)
