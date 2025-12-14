from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa import constants
from majsoulrpa.config_input._common import _to_kebab


class Endpoint(BaseModel):
    model_config = ConfigDict(extra="forbid", alias_generator=_to_kebab)

    browser_address: str = Field(constants.DEFAULT_BROWSER_ADDRESS)
    client_address: str = Field(constants.DEFAULT_CLIENT_ADDRESS)
