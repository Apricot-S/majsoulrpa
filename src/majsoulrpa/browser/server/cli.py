import argparse
import sys
from dataclasses import dataclass
from pathlib import Path

from majsoulrpa import netutils
from majsoulrpa.browser.server.config import Config
from majsoulrpa.browser.server.engine import Option
from majsoulrpa.browser.server.runtime import run_processes
from majsoulrpa.constants import (
    DEFAULT_CLIENT_ADDRESS,
    DEFAULT_PROXY_PORT,
    DEFAULT_REMOTE_PORT,
    DEFAULT_SNIFFER_PORT,
    DEFAULT_VIEWPORT_HEIGHT,
)
from majsoulrpa.exceptions import UserInputError

VIEWPORT_HEIGHT_CHOICES = (540, 720, 900, 1080, 1440)


@dataclass(frozen=True)
class CommandLineArgs:
    client_address: str = DEFAULT_CLIENT_ADDRESS
    remote_port: int = DEFAULT_REMOTE_PORT
    sniffer_port: int = DEFAULT_SNIFFER_PORT
    proxy_port: int = DEFAULT_PROXY_PORT

    window_left: int = 0
    window_top: int = 0
    viewport_height: int = DEFAULT_VIEWPORT_HEIGHT
    headless: bool = False
    user_data_dir: Path | None = None

    def to_config(self) -> Config:
        return Config(
            netutils.parse_ip_address(self.client_address),
            netutils.validate_user_port(self.remote_port),
            netutils.validate_user_port(self.sniffer_port),
            netutils.validate_user_port(self.proxy_port),
        )

    def to_option(self) -> Option:
        return Option(
            user_data_dir=self.user_data_dir,
            window_left=self.window_left,
            window_top=self.window_top,
            viewport_height=self.viewport_height,
            headless=self.headless,
        )


def get_command_line_args() -> CommandLineArgs:
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

    return CommandLineArgs(
        client_address=args.client_address,
        remote_port=args.remote_port,
        sniffer_port=args.sniffer_port,
        proxy_port=args.proxy_port,
        window_left=args.window_left,
        window_top=args.window_top,
        viewport_height=args.viewport_height,
        headless=args.headless,
        user_data_dir=args.user_data_dir,
    )


def main() -> None:
    try:
        args = get_command_line_args()
        config = args.to_config()
        option = args.to_option()
        run_processes(config, option)
    except UserInputError as e:
        print(e, file=sys.stderr)  # noqa: T201
        sys.exit(1)


if __name__ == "__main__":
    main()
