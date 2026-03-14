from pathlib import Path
from subprocess import Popen

from majsoulrpa.browser.server import Config
from majsoulrpa.browser.server.runtime import run_browser_server
from majsoulrpa.browser.server.sniffer import run_sniffer
from majsoulrpa.config_input import Browser, ConfigInput

ADDON_PATH = Path(__file__).parent / "addon.py"


def archiver_runner(config: Config) -> Popen:
    return run_sniffer(config, ADDON_PATH)


def main() -> None:
    cfg_in = ConfigInput(browser=Browser(viewport_height=720, headless=True))
    config = cfg_in.build_browser_config()
    option = cfg_in.build_browser_option()
    run_browser_server(config, option, sniffer_runner=archiver_runner)


if __name__ == "__main__":
    main()
