from copy import deepcopy

from majsoulrpa import constants
from majsoulrpa.config_input.config import ConfigInput


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
