from pathlib import Path

from pytest_mock import MockerFixture

from majsoulrpa.config import get_config


def test_get_config_not_exist(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {}

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_empty(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {}

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_single(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    remote_host = "127.0.0.1"
    [majsoulrpa.authentication]
    email_address = "your_email_address@example.cfg"
    [majsoulrpa.port]
    remote_port = 19222
    proxy_port = 8080
    message_queue_port = 37247
    [majsoulrpa.browser]
    initial_position = { left = 100, top = 100 }
    viewport_height = 720
    headless = false
    user_data_dir = "./user_data"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected = {
        "remote_host": "127.0.0.1",
        "authentication": {
            "email_address": "your_email_address@example.cfg",
        },
        "port": {
            "remote_port": 19222,
            "proxy_port": 8080,
            "message_queue_port": 37247,
        },
        "browser": {
            "initial_position": {
                "left": 100,
                "top": 100,
            },
            "viewport_height": 720,
            "headless": False,
            "user_data_dir": "./user_data",
        },
    }

    actual = get_config(config_path)
    assert actual == expected
