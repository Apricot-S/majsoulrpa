from pathlib import Path

import pytest
from pydantic import ValidationError

from majsoulrpa.config import AppConfig, BrowserConfig, EndpointConfig


def test_app_config_defaults_to_local_combined_runtime() -> None:
    config = AppConfig()

    assert config.endpoint.browser_host == "127.0.0.1"
    assert config.endpoint.client_host == "127.0.0.1"
    assert config.endpoint.remote_port == 19222
    assert config.endpoint.sniffer_port == 37247
    assert config.browser.viewport_height == 1080
    assert config.browser.headless is False
    assert config.browser.user_data_dir is None


def test_endpoint_host_must_not_be_empty() -> None:
    with pytest.raises(ValidationError, match="browser_host"):
        EndpointConfig(browser_host="")


@pytest.mark.parametrize("port", [1023, 49152])
def test_endpoint_port_must_be_user_port(port: int) -> None:
    with pytest.raises(ValidationError, match="remote_port"):
        EndpointConfig(remote_port=port)


def test_browser_viewport_height_must_be_supported() -> None:
    with pytest.raises(ValidationError, match="viewport_height"):
        BrowserConfig.model_validate({"viewport_height": 900})


def test_browser_user_data_dir_accepts_path() -> None:
    config = BrowserConfig(user_data_dir=Path("user-data"))

    assert config.user_data_dir == Path("user-data")
