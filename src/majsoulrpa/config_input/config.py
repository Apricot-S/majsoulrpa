from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa import netutils
from majsoulrpa.browser.server import Config as BrowserConfig
from majsoulrpa.browser.server.engine import Option as BrowserOption
from majsoulrpa.config_input._common import _to_kebab
from majsoulrpa.config_input.browser import Browser
from majsoulrpa.config_input.endpoint import Endpoint
from majsoulrpa.rpa_client import Config as ClientConfig


class ConfigInput(BaseModel):
    model_config = ConfigDict(
        alias_generator=_to_kebab,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    endpoint: Endpoint = Field(default_factory=Endpoint)
    browser: Browser = Field(default_factory=Browser)

    def build_client_config(self) -> ClientConfig:
        return ClientConfig(
            netutils.parse_ip_address(self.endpoint.browser_address),
            netutils.validate_user_port(self.endpoint.remote_port),
            netutils.validate_user_port(self.endpoint.sniffer_port),
        )

    def build_browser_config(self) -> BrowserConfig:
        return BrowserConfig(
            netutils.parse_ip_address(self.endpoint.client_address),
            netutils.validate_user_port(self.endpoint.remote_port),
            netutils.validate_user_port(self.endpoint.sniffer_port),
            netutils.validate_user_port(self.endpoint.proxy_port),
        )

    def build_browser_option(self) -> BrowserOption:
        return BrowserOption(
            self.browser.user_data_dir,
            self.browser.window_left,
            self.browser.window_top,
            self.browser.viewport_height,
            self.browser.headless,
        )
