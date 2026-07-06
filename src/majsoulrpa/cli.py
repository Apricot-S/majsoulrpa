import argparse
import asyncio
from collections.abc import Callable, Coroutine
from pathlib import Path
from typing import Any

from majsoulrpa import __version__
from majsoulrpa.browser import run_browser_host as default_run_browser_host
from majsoulrpa.config import AppConfig

RunBrowserHost = Callable[[AppConfig], Coroutine[Any, Any, None]]


def main(
    argv: list[str] | None = None,
    *,
    run_browser_host: RunBrowserHost = default_run_browser_host,
) -> int:
    parser = argparse.ArgumentParser(
        prog="majsoulrpa-browser",
        description="MajsoulRPA browser host entry point.",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--config",
        type=Path,
        help="Path to TOML config file.",
    )
    parser.add_argument("--browser-host")
    parser.add_argument("--remote-port", type=int)
    parser.add_argument("--viewport-height", type=int)
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=None,
    )
    parser.add_argument("--user-data-dir", type=Path)
    parser.add_argument("--window-left", type=int)
    parser.add_argument("--window-top", type=int)
    args = parser.parse_args(argv)

    config = (
        AppConfig.from_toml_file(args.config)
        if args.config is not None
        else AppConfig()
    )
    config = _apply_overrides(config, args)
    try:
        asyncio.run(run_browser_host(config))
    except KeyboardInterrupt:
        return 130
    return 0


def _apply_overrides(config: AppConfig, args: argparse.Namespace) -> AppConfig:
    endpoint_updates = {}
    if args.browser_host is not None:
        endpoint_updates["browser_host"] = args.browser_host
    if args.remote_port is not None:
        endpoint_updates["remote_port"] = args.remote_port

    browser_updates = {}
    if args.viewport_height is not None:
        browser_updates["viewport_height"] = args.viewport_height
    if args.headless is not None:
        browser_updates["headless"] = args.headless
    if args.user_data_dir is not None:
        browser_updates["user_data_dir"] = args.user_data_dir
    if args.window_left is not None:
        browser_updates["window_left"] = args.window_left
    if args.window_top is not None:
        browser_updates["window_top"] = args.window_top

    if not endpoint_updates and not browser_updates:
        return config

    config_data = config.model_dump()
    if endpoint_updates:
        config_data["endpoint"] |= endpoint_updates
    if browser_updates:
        config_data["browser"] |= browser_updates
    return AppConfig.model_validate(config_data)
