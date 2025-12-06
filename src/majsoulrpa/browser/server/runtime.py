import asyncio

from majsoulrpa.browser.server import core
from majsoulrpa.browser.server.config import Config
from majsoulrpa.browser.server.engine import (
    BrowserEngineRunner,
    Option,
    run_browser_engine,
)
from majsoulrpa.browser.server.sniffer import SnifferRunner, run_sniffer
from majsoulrpa.sniffer import ADDON_PATH


def run_processes_impl(
    config: Config,
    option: Option,
    server_runner: core.ServerRunner,
    browser_engine_runner: BrowserEngineRunner,
    sniffer_runner: SnifferRunner,
) -> None:
    sniffer_process = sniffer_runner(config)

    try:
        asyncio.run(browser_engine_runner(config, option, server_runner))
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()


def run_processes(config: Config, option: Option) -> None:
    run_processes_impl(
        config,
        option,
        core.run_server,
        run_browser_engine,
        lambda c: run_sniffer(c, ADDON_PATH),
    )
