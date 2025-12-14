from pathlib import Path
from subprocess import Popen

from majsoulrpa.browser.server import Config
from majsoulrpa.browser.server.cli import CommandLineArgs
from majsoulrpa.browser.server.runtime import run_browser_server
from majsoulrpa.browser.server.sniffer import run_sniffer

ADDON_PATH = Path(__file__).parent / "fetch_log_addon.py"


def main() -> None:
    def archiver_runner(config: Config) -> Popen:
        return run_sniffer(config, ADDON_PATH)

    args = CommandLineArgs(viewport_height=720, headless=True)
    config = args.to_config()
    option = args.to_option()
    run_browser_server(config, option, sniffer_runner=archiver_runner)


if __name__ == "__main__":
    main()
