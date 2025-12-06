import asyncio

from majsoulrpa.browser.server import core, engine, sniffer
from majsoulrpa.browser.server.config import Config
from majsoulrpa.sniffer import ADDON_PATH


def run_browser_server(
    config: Config,
    option: engine.Option,
    server_runner: core.ServerRunner | None = None,
    browser_engine_runner: engine.BrowserEngineRunner | None = None,
    sniffer_runner: sniffer.SnifferRunner | None = None,
) -> None:
    server_runner = server_runner or core.run_server
    browser_engine_runner = browser_engine_runner or engine.run_browser_engine
    sniffer_runner = sniffer_runner or (
        lambda c: sniffer.run_sniffer(c, ADDON_PATH)
    )

    sniffer_process = sniffer_runner(config)

    try:
        asyncio.run(browser_engine_runner(config, option, server_runner))
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()
