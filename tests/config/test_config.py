import io
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


def test_get_config_name(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    name = "config1"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {
        "name": "config1",
    }

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_remote_host(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    remote_host = "127.0.0.1"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {
        "remote_host": "127.0.0.1",
    }

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_authentication_manual(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    [majsoulrpa.authentication]
    email_address = "your_email_address@example.cfg"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {
        "authentication": {
            "email_address": "your_email_address@example.cfg",
        },
    }

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_authentication_imap(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    [majsoulrpa.authentication]
    email_address = "your_email_address_two@example.cfg"
    imap_server = "imap.server.cfg"
    password = "app_password"
    mail_folder = "INBOX"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {
        "authentication": {
            "email_address": "your_email_address_two@example.cfg",
            "imap_server": "imap.server.cfg",
            "password": "app_password",
            "mail_folder": "INBOX",
        },
    }

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_authentication_s3_wo_aws_profile(
    mocker: MockerFixture,
) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    [majsoulrpa.authentication]
    method = "s3"
    email_address = "your_email_address_three@example.cfg"
    bucket_name = "your-example-bucket1"
    key_prefix = "verification-email"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {
        "authentication": {
            "method": "s3",
            "email_address": "your_email_address_three@example.cfg",
            "bucket_name": "your-example-bucket1",
            "key_prefix": "verification-email",
        },
    }

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_authentication_s3_w_aws_profile(
    mocker: MockerFixture,
) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    [majsoulrpa.authentication]
    method = "s3"
    email_address = "your_email_address_three@example.cfg"
    bucket_name = "your-example-bucket1"
    key_prefix = "verification-email"
    aws_profile = "foobar"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {
        "authentication": {
            "method": "s3",
            "email_address": "your_email_address_three@example.cfg",
            "bucket_name": "your-example-bucket1",
            "key_prefix": "verification-email",
            "aws_profile": "foobar",
        },
    }

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_port(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
    [majsoulrpa.port]
    remote_port = 19222
    proxy_port = 8080
    message_queue_port = 37247
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )

    expected: dict = {
        "port": {
            "remote_port": 19222,
            "proxy_port": 8080,
            "message_queue_port": 37247,
        },
    }

    actual = get_config(config_path)
    assert actual == expected


def test_get_config_browser(mocker: MockerFixture) -> None:
    config_path = Path("./config.toml")
    config_data = b"""
    [[majsoulrpa]]
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

    expected: dict = {
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


def test_get_config_multiple(mocker: MockerFixture) -> None:
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

    [[majsoulrpa]]
    name = "Desktop headless IMAP 1920 x 1080"
    [majsoulrpa.authentication]
    email_address = "your_email_address_two@example.cfg"
    imap_server = "imap.server.cfg"
    password = "app_password"
    mail_folder = "INBOX"
    [majsoulrpa.browser]
    initial_position = { left = -2150, top = -360 }
    headless = true
    user_data_dir = "./user_data"
    """

    mocker.patch(
        "pathlib.Path.open",
        new_callable=mocker.mock_open,
        read_data=config_data,
    )
    mocker.patch("sys.stdin", io.StringIO("0\n"))

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

    mocker.patch("sys.stdin", io.StringIO("1\n"))

    expected = {
        "name": "Desktop headless IMAP 1920 x 1080",
        "authentication": {
            "email_address": "your_email_address_two@example.cfg",
            "imap_server": "imap.server.cfg",
            "password": "app_password",
            "mail_folder": "INBOX",
        },
        "browser": {
            "initial_position": {
                "left": -2150,
                "top": -360,
            },
            "headless": True,
            "user_data_dir": "./user_data",
        },
    }

    actual = get_config(config_path)
    assert actual == expected
