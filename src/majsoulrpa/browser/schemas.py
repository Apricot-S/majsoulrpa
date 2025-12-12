from enum import StrEnum, auto
from typing import Annotated, Literal

from pydantic import BaseModel, Field, TypeAdapter


class Action(StrEnum):
    RESOLUTION = auto()
    MOVE_MOUSE = auto()
    CLICK_MOUSE = auto()
    PRESS_KEY = auto()
    TYPE_KEY = auto()
    SCREENSHOT = auto()
    LOG = auto()
    RELOAD = auto()
    QUIT = auto()


# --- Requests ---


class ResolutionRequest(BaseModel):
    action: Literal[Action.RESOLUTION] = Action.RESOLUTION


class MoveMouseRequest(BaseModel):
    action: Literal[Action.MOVE_MOUSE] = Action.MOVE_MOUSE
    x: float = Field(..., ge=0.0)
    y: float = Field(..., ge=0.0)


class ClickMouseRequest(BaseModel):
    action: Literal[Action.CLICK_MOUSE] = Action.CLICK_MOUSE
    x: float = Field(..., ge=0.0)
    y: float = Field(..., ge=0.0)
    delay: float = Field(..., ge=0.0)


class PressKeyRequest(BaseModel):
    action: Literal[Action.PRESS_KEY] = Action.PRESS_KEY
    key: str
    delay: float = Field(..., ge=0.0)


class TypeKeyRequest(BaseModel):
    action: Literal[Action.TYPE_KEY] = Action.TYPE_KEY
    text: str
    delay: float = Field(..., ge=0.0)


class ScreenshotRequest(BaseModel):
    action: Literal[Action.SCREENSHOT] = Action.SCREENSHOT


class LogRequest(BaseModel):
    action: Literal[Action.LOG] = Action.LOG
    log_id: str


class ReloadRequest(BaseModel):
    action: Literal[Action.RELOAD] = Action.RELOAD


class QuitRequest(BaseModel):
    action: Literal[Action.QUIT] = Action.QUIT


type Request = Annotated[
    ResolutionRequest
    | MoveMouseRequest
    | ClickMouseRequest
    | PressKeyRequest
    | TypeKeyRequest
    | ScreenshotRequest
    | LogRequest
    | ReloadRequest
    | QuitRequest,
    Field(discriminator="action"),
]

REQUEST_ADAPTER: TypeAdapter[Request] = TypeAdapter(Request)


# --- Responses ---


class ResolutionResponse(BaseModel):
    action: Literal[Action.RESOLUTION] = Action.RESOLUTION
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)
    scale: float = Field(..., gt=0.0)


class MoveMouseResponse(BaseModel):
    action: Literal[Action.MOVE_MOUSE] = Action.MOVE_MOUSE
    x: float = Field(..., ge=0.0)
    y: float = Field(..., ge=0.0)


class ClickMouseResponse(BaseModel):
    action: Literal[Action.CLICK_MOUSE] = Action.CLICK_MOUSE
    x: float = Field(..., ge=0.0)
    y: float = Field(..., ge=0.0)
    delay: float = Field(..., ge=0.0)


class PressKeyResponse(BaseModel):
    action: Literal[Action.PRESS_KEY] = Action.PRESS_KEY
    key: str
    delay: float = Field(..., ge=0.0)


class TypeKeyResponse(BaseModel):
    action: Literal[Action.TYPE_KEY] = Action.TYPE_KEY
    text: str
    delay: float = Field(..., ge=0.0)


class ScreenshotResponse(BaseModel):
    action: Literal[Action.SCREENSHOT] = Action.SCREENSHOT
    image: str


class LogResponse(BaseModel):
    action: Literal[Action.LOG] = Action.LOG


class ReloadResponse(BaseModel):
    action: Literal[Action.RELOAD] = Action.RELOAD


class QuitResponse(BaseModel):
    action: Literal[Action.QUIT] = Action.QUIT


class ErrorResponse(BaseModel):
    action: Literal["error"] = "error"
    message: str


type Response = Annotated[
    ResolutionResponse
    | MoveMouseResponse
    | ClickMouseResponse
    | PressKeyResponse
    | TypeKeyResponse
    | ScreenshotResponse
    | LogResponse
    | ReloadResponse
    | QuitResponse
    | ErrorResponse,
    Field(discriminator="action"),
]

RESPONSE_ADAPTER: TypeAdapter[Response] = TypeAdapter(Response)
