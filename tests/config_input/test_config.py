from copy import deepcopy

from majsoulrpa import constants, netutils
from majsoulrpa.browser.server import Config as BrowserConfig
from majsoulrpa.browser.server.engine import Option as BrowserOption
from majsoulrpa.config_input.browser import Browser
from majsoulrpa.config_input.config import ConfigInput
from majsoulrpa.config_input.endpoint import Endpoint
from majsoulrpa.rpa_client import Config as ClientConfig


def test_defaults_to_dict() -> None:
    expected: dict = {
        "endpoint": {
            "browser-address": constants.DEFAULT_BROWSER_ADDRESS,
            "client-address": constants.DEFAULT_CLIENT_ADDRESS,
            "remote-port": constants.DEFAULT_REMOTE_PORT,
            "sniffer-port": constants.DEFAULT_SNIFFER_PORT,
            "proxy-port": constants.DEFAULT_PROXY_PORT,
        },
        "browser": {
            "window-left": 0,
            "window-top": 0,
            "viewport-height": constants.DEFAULT_VIEWPORT_HEIGHT,
            "headless": False,
            "user-data-dir": None,
        },
    }
    assert ConfigInput().model_dump() == expected


def test_from_init() -> None:
    actual = ConfigInput(
        endpoint=Endpoint(proxy_port=8081),
        browser=Browser(headless=True),
    )

    expected = ConfigInput.model_validate(
        {
            "endpoint": {
                "browser-address": constants.DEFAULT_BROWSER_ADDRESS,
                "client-address": constants.DEFAULT_CLIENT_ADDRESS,
                "remote-port": constants.DEFAULT_REMOTE_PORT,
                "sniffer-port": constants.DEFAULT_SNIFFER_PORT,
                "proxy-port": 8081,
            },
            "browser": {
                "window-left": 0,
                "window-top": 0,
                "viewport-height": constants.DEFAULT_VIEWPORT_HEIGHT,
                "headless": True,
                "user-data-dir": None,
            },
        },
    )

    assert actual == expected


def test_ignore_extra() -> None:
    expected: dict = {
        "endpoint": {
            "browser-address": constants.DEFAULT_BROWSER_ADDRESS,
            "client-address": constants.DEFAULT_CLIENT_ADDRESS,
            "remote-port": constants.DEFAULT_REMOTE_PORT,
            "sniffer-port": constants.DEFAULT_SNIFFER_PORT,
            "proxy-port": constants.DEFAULT_PROXY_PORT,
        },
        "browser": {
            "window-left": 0,
            "window-top": 0,
            "viewport-height": constants.DEFAULT_VIEWPORT_HEIGHT,
            "headless": False,
            "user-data-dir": None,
        },
    }

    input_dict = deepcopy(expected)
    input_dict["extra"] = {"extra1": 1}
    actual = ConfigInput().model_validate(input_dict).model_dump()

    assert actual == expected


def test_build_client_config_default() -> None:
    expected = ClientConfig(
        netutils.parse_ip_address(constants.DEFAULT_BROWSER_ADDRESS),
        netutils.validate_user_port(constants.DEFAULT_REMOTE_PORT),
        netutils.validate_user_port(constants.DEFAULT_SNIFFER_PORT),
    )
    assert ConfigInput().build_client_config() == expected


def test_build_client_config_custom() -> None:
    actual = ConfigInput(
        endpoint=Endpoint(browser_address="127.0.0.2"),
    ).build_client_config()

    expected = ClientConfig(
        netutils.parse_ip_address("127.0.0.2"),
        netutils.validate_user_port(constants.DEFAULT_REMOTE_PORT),
        netutils.validate_user_port(constants.DEFAULT_SNIFFER_PORT),
    )
    assert actual == expected


def test_build_browser_config_default() -> None:
    expected = BrowserConfig(
        netutils.parse_ip_address(constants.DEFAULT_CLIENT_ADDRESS),
        netutils.validate_user_port(constants.DEFAULT_REMOTE_PORT),
        netutils.validate_user_port(constants.DEFAULT_SNIFFER_PORT),
        netutils.validate_user_port(constants.DEFAULT_PROXY_PORT),
    )
    assert ConfigInput().build_browser_config() == expected


def test_build_browser_config_custom() -> None:
    actual = ConfigInput(
        endpoint=Endpoint(client_address="127.0.0.2"),
    ).build_browser_config()

    expected = BrowserConfig(
        netutils.parse_ip_address("127.0.0.2"),
        netutils.validate_user_port(constants.DEFAULT_REMOTE_PORT),
        netutils.validate_user_port(constants.DEFAULT_SNIFFER_PORT),
        netutils.validate_user_port(constants.DEFAULT_PROXY_PORT),
    )
    assert actual == expected


def test_build_browser_option_default() -> None:
    expected = BrowserOption(
        None,
        0,
        0,
        constants.DEFAULT_VIEWPORT_HEIGHT,
        headless=False,
    )
    assert ConfigInput().build_browser_option() == expected


def test_build_browser_option_custom() -> None:
    actual = ConfigInput(
        browser=Browser(viewport_height=720),
    ).build_browser_option()

    expected = BrowserOption(None, 0, 0, 720, headless=False)
    assert actual == expected
