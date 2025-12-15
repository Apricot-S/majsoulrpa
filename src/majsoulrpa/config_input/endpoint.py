from pydantic import BaseModel, ConfigDict

from majsoulrpa import constants
from majsoulrpa.config_input._common import _to_kebab


class Endpoint(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        alias_generator=_to_kebab,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    browser_address: str = constants.DEFAULT_BROWSER_ADDRESS
    client_address: str = constants.DEFAULT_CLIENT_ADDRESS
    remote_port: int = constants.DEFAULT_REMOTE_PORT
    sniffer_port: int = constants.DEFAULT_SNIFFER_PORT
    proxy_port: int = constants.DEFAULT_PROXY_PORT
