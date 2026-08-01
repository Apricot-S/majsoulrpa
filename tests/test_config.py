from pathlib import Path
from textwrap import dedent

import pytest
from pydantic import ValidationError

from majsoulrpa.config import (
    AppConfig,
    BrowserConfig,
    EndpointConfig,
    YostarEmailConfig,
    YostarEmailS3Config,
)


def test_app_config_defaults_to_local_combined_runtime() -> None:
    config = AppConfig()

    assert config.endpoint.browser_host == "127.0.0.1"
    assert config.endpoint.client_host == "127.0.0.1"
    assert config.endpoint.remote_port == 19222
    assert config.endpoint.sniffer_port == 37247
    assert config.browser.viewport_height == 1080
    assert config.browser.headless is False
    assert config.browser.user_data_dir is None
    assert config.yostar_email is None


@pytest.mark.parametrize("host_key", ["browser_host", "client_host"])
def test_endpoint_host_must_not_be_empty(host_key: str) -> None:
    with pytest.raises(ValidationError, match=host_key):
        EndpointConfig.model_validate({host_key: ""})


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


def test_config_example_uses_safe_yostar_email_placeholders() -> None:
    config_path = (
        Path(__file__).parents[1] / "examples" / "config.example.toml"
    )

    config = AppConfig.from_toml_file(config_path)

    assert config.endpoint == EndpointConfig()
    assert config.browser == BrowserConfig()
    assert config.yostar_email == YostarEmailConfig(
        email_address="user@example.com",
        s3=YostarEmailS3Config(
            bucket_name="example-bucket",
            key_prefix="example-prefix/",
        ),
    )


def test_app_config_can_be_loaded_from_toml_text() -> None:
    config = AppConfig.from_toml_text(
        dedent(
            """
            [endpoint]
            browser_host = "192.0.2.10"
            client_host = "192.0.2.20"
            remote_port = 12000
            sniffer_port = 12001

            [browser]
            window_left = 100
            window_top = 200
            viewport_height = 720
            headless = true
            user_data_dir = "user-data"
            """,
        ),
    )

    assert config.endpoint.browser_host == "192.0.2.10"
    assert config.endpoint.client_host == "192.0.2.20"
    assert config.endpoint.remote_port == 12000
    assert config.endpoint.sniffer_port == 12001
    assert config.browser.window_left == 100
    assert config.browser.window_top == 200
    assert config.browser.viewport_height == 720
    assert config.browser.headless is True
    assert config.browser.user_data_dir == Path("user-data")


def test_app_config_can_be_loaded_from_toml_file(tmp_path: Path) -> None:
    config_file = tmp_path / "config.toml"
    config_file.write_text(
        "[browser]\nviewport_height = 1440\n",
        encoding="utf-8",
    )

    config = AppConfig.from_toml_file(config_file)

    assert config.browser.viewport_height == 1440


def test_yostar_email_s3_config_can_be_loaded_from_toml() -> None:
    config = AppConfig.from_toml_text(
        dedent(
            """
            [yostar_email]
            email_address = "user@example.com"

            [yostar_email.s3]
            bucket_name = "example-bucket"
            key_prefix = "example-prefix/"
            aws_profile = "example-profile"
            """,
        ),
    )

    assert config.yostar_email is not None
    assert config.yostar_email.email_address == "user@example.com"
    assert config.yostar_email.s3 is not None
    assert config.yostar_email.s3.bucket_name == "example-bucket"
    assert config.yostar_email.s3.key_prefix == "example-prefix/"
    assert config.yostar_email.s3.aws_profile == "example-profile"
    assert "user@example.com" not in repr(config)


def test_yostar_email_config_does_not_require_s3_config() -> None:
    config = AppConfig.from_toml_text(
        dedent(
            """
            [yostar_email]
            email_address = "user@example.com"
            """,
        ),
    )

    assert config.yostar_email == YostarEmailConfig(
        email_address="user@example.com",
    )
    assert config.yostar_email is not None
    assert config.yostar_email.s3 is None


@pytest.mark.parametrize(
    "config_text",
    [
        "[yostar_email]\nemail_address = ''\n",
        (
            "[yostar_email]\nemail_address = 'user@example.com'\n"
            "[yostar_email.s3]\nbucket_name = ''\n"
        ),
    ],
)
def test_yostar_email_config_rejects_empty_required_values(
    config_text: str,
) -> None:
    with pytest.raises(ValidationError):
        AppConfig.from_toml_text(config_text)


def test_app_config_rejects_unknown_toml_key() -> None:
    with pytest.raises(ValidationError, match="unexpected"):
        AppConfig.from_toml_text("unexpected = true\n")


@pytest.mark.parametrize(
    "config_text",
    [
        '[endpoint]\nremote_port = "12000"\n',
        '[endpoint]\nsniffer_port = "12001"\n',
        '[browser]\nwindow_left = "100"\n',
        '[browser]\nwindow_top = "200"\n',
        '[browser]\nviewport_height = "720"\n',
        "[browser]\nheadless = 1\n",
    ],
)
def test_app_config_rejects_toml_scalar_type_coercion(
    config_text: str,
) -> None:
    with pytest.raises(ValidationError):
        AppConfig.from_toml_text(config_text)
