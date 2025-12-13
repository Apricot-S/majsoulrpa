import asyncio
import warnings

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
    # On Windows, the `ProactorEventLoop` does not implement
    # the add_reader family of methods.
    # When using `zmq.asyncio`, Tornado automatically registers
    # a selector thread to provide add_reader support.
    # This behavior always triggers a `RuntimeWarning`,
    # even though it is harmless.
    # Since Tornado is functioning correctly and the warning only causes
    # confusion, we suppress it here to keep the output clean.
    warnings.filterwarnings(
        "ignore",
        message="Proactor event loop does not implement add_reader",
        category=RuntimeWarning,
        module="zmq",
    )

    if server_runner is None:
        server_runner = core.run_server
    if browser_engine_runner is None:
        browser_engine_runner = engine.run_browser_engine
    if sniffer_runner is None:
        sniffer_runner = lambda c: sniffer.run_sniffer(c, ADDON_PATH)  # noqa: E731

    sniffer_process = sniffer_runner(config)

    try:
        asyncio.run(browser_engine_runner(config, option, server_runner))
    finally:
        if sniffer_process.poll() is None:
            sniffer_process.terminate()
        sniffer_process.wait()
