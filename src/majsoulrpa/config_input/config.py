from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa.config_input._common import _to_kebab
from majsoulrpa.config_input.browser import Browser
from majsoulrpa.config_input.endpoint import Endpoint


class ConfigInput(BaseModel):
    model_config = ConfigDict(
        alias_generator=_to_kebab,
        serialize_by_alias=True,
    )

    endpoint: Endpoint = Field(default_factory=Endpoint)
    browser: Browser = Field(default_factory=Browser)
