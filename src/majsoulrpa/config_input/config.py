from pydantic import BaseModel, ConfigDict

from majsoulrpa.config_input._common import _to_kebab
from majsoulrpa.config_input.endpoint import Endpoint


class ConfigInput(BaseModel):
    model_config = ConfigDict(alias_generator=_to_kebab)

    endpoint: Endpoint
