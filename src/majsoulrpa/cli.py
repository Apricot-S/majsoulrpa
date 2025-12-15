import argparse
import sys
from pathlib import Path

from majsoulrpa import config_input
from majsoulrpa.browser.server.runtime import run_browser_server
from majsoulrpa.config_input import ConfigInput
from majsoulrpa.constants import (
    DEFAULT_CLIENT_ADDRESS,
    DEFAULT_PROXY_PORT,
    DEFAULT_REMOTE_PORT,
    DEFAULT_SNIFFER_PORT,
    DEFAULT_VIEWPORT_HEIGHT,
)
from majsoulrpa.exceptions import UserInputError

VIEWPORT_HEIGHT_CHOICES = (720, 1080, 1440)


def get_command_line_args() -> ConfigInput:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--client-address",
        type=str,
        default=DEFAULT_CLIENT_ADDRESS,
    )
    parser.add_argument(
        "--remote-port",
        type=int,
        default=DEFAULT_REMOTE_PORT,
    )
    parser.add_argument(
        "--sniffer-port",
        type=int,
        default=DEFAULT_SNIFFER_PORT,
    )
    parser.add_argument(
        "--proxy-port",
        type=int,
        default=DEFAULT_PROXY_PORT,
    )

    parser.add_argument("--window-left", type=int, default=0)
    parser.add_argument("--window-top", type=int, default=0)
    parser.add_argument(
        "--viewport-height",
        type=int,
        choices=VIEWPORT_HEIGHT_CHOICES,
        default=DEFAULT_VIEWPORT_HEIGHT,
    )
    parser.add_argument("--headless", action="store_true")
    parser.add_argument("--user-data-dir", type=Path, default=None)

    args = parser.parse_args()

    return ConfigInput(
        endpoint=config_input.Endpoint(
            client_address=args.client_address,
            remote_port=args.remote_port,
            sniffer_port=args.sniffer_port,
            proxy_port=args.proxy_port,
        ),
        browser=config_input.Browser(
            window_left=args.window_left,
            window_top=args.window_top,
            viewport_height=args.viewport_height,
            headless=args.headless,
            user_data_dir=args.user_data_dir,
        ),
    )


def main() -> None:
    try:
        config_input = get_command_line_args()
        config = config_input.build_browser_config()
        option = config_input.build_browser_option()
        run_browser_server(config, option)
    except UserInputError as e:
        print(e, file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
