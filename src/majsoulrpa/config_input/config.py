from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa import netutils
from majsoulrpa.browser.server import Config as BrowserConfig
from majsoulrpa.browser.server.engine_option import Option as BrowserOption
from majsoulrpa.config_input._common import _to_kebab
from majsoulrpa.config_input.browser import Browser
from majsoulrpa.config_input.endpoint import Endpoint
from majsoulrpa.config_input.yostar_login import YostarLogin
from majsoulrpa.rpa_client import Config as ClientConfig
from majsoulrpa.yostar_login import Config as YostarLoginConfig
from majsoulrpa.yostar_login.config import S3Config


class ConfigInput(BaseModel):
    model_config = ConfigDict(
        alias_generator=_to_kebab,
        validate_by_name=True,
        serialize_by_alias=True,
    )

    endpoint: Endpoint = Field(default_factory=Endpoint)
    browser: Browser = Field(default_factory=Browser)
    yostar_login: YostarLogin = Field(default_factory=YostarLogin)

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

    def build_yostar_login_config(self) -> YostarLoginConfig:
        if self.yostar_login.s3 is None:
            s3 = None
        else:
            s3 = S3Config(
                self.yostar_login.s3.bucket_name,
                self.yostar_login.s3.key_prefix,
                self.yostar_login.s3.aws_profile,
            )

        return YostarLoginConfig(self.yostar_login.email_address, s3)
