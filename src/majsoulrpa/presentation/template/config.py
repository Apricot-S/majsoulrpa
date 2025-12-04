from pydantic import BaseModel, Field


class Region(BaseModel):
    left: int = Field(..., ge=0)
    top: int = Field(..., ge=0)
    width: int = Field(..., gt=0)
    height: int = Field(..., gt=0)


class Margin(BaseModel):
    left: int = Field(..., ge=0)
    right: int = Field(..., ge=0)
    top: int = Field(..., ge=0)
    bottom: int = Field(..., ge=0)


class Settings(BaseModel):
    threshold: float = Field(..., gt=0.0, lt=1.0)


class Config(BaseModel):
    region: Region
    margin: Margin
    settings: Settings
