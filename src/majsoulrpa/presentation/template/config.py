import tomllib
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, Field


class Region(BaseModel):
    left: Annotated[int, Field(..., ge=0)]
    top: Annotated[int, Field(..., ge=0)]
    width: Annotated[int, Field(..., gt=0)]
    height: Annotated[int, Field(..., gt=0)]


class Margin(BaseModel):
    left: Annotated[int, Field(..., ge=0)]
    right: Annotated[int, Field(..., ge=0)]
    top: Annotated[int, Field(..., ge=0)]
    bottom: Annotated[int, Field(..., ge=0)]


class Settings(BaseModel):
    threshold: Annotated[float, Field(..., gt=0.0, lt=1.0)]


class Config(BaseModel):
    region: Region
    margin: Margin
    settings: Settings

    @classmethod
    def from_file(cls, path: Path) -> "Config":
        with path.open("rb") as f:
            data = tomllib.load(f)
        return cls.model_validate(data)
