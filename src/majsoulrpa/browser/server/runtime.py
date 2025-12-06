import asyncio

from majsoulrpa.browser.server import core, engine, sniffer
from majsoulrpa.browser.server.config import Config
from majsoulrpa.sniffer import ADDON_PATH


def run_browser_server_impl(
    config: Config,
    option: engine.Option,
    server_runner: core.ServerRunner,
    browser_engine_runner: engine.BrowserEngineRunner,
    sniffer_runner: sniffer.SnifferRunner,
) -> None:
    sniffer_process = sniffer_runner(config)

    try:
        asyncio.run(browser_engine_runner(config, option, server_runner))
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()


def run_browser_server(config: Config, option: engine.Option) -> None:
    run_browser_server_impl(
        config,
        option,
        core.run_server,
        engine.run_browser_engine,
        lambda c: sniffer.run_sniffer(c, ADDON_PATH),
    )
