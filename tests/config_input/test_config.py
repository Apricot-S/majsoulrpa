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
    actual = ConfigInput.model_validate({}).model_dump()
    assert actual == expected
