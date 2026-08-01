from pathlib import Path

import pytest
from pydantic import ValidationError

from majsoulrpa import __version__
from majsoulrpa.cli import main
from majsoulrpa.config import AppConfig


def test_browser_cli_entry_point_accepts_empty_arguments() -> None:
    called_configs = []

    async def run_browser_host(config) -> None:  # noqa: ANN001
        called_configs.append(config)

    assert main([], run_browser_host=run_browser_host) == 0
    assert len(called_configs) == 1


def test_browser_cli_accepts_config_file_and_overrides(tmp_path: Path) -> None:
    config_path = tmp_path / "config.toml"
    config_path.write_text(
        """
[endpoint]
browser_host = "192.0.2.10"
client_host = "192.0.2.20"
remote_port = 12000

[browser]
viewport_height = 720
headless = true
""".strip(),
        encoding="utf-8",
    )
    called_configs = []

    async def run_browser_host(config) -> None:  # noqa: ANN001
        called_configs.append(config)

    result = main(
        [
            "--config",
            str(config_path),
            "--client-host",
            "127.0.0.1",
            "--remote-port",
            "13000",
            "--viewport-height",
            "1080",
            "--no-headless",
            "--user-data-dir",
            str(tmp_path / "user-data"),
            "--window-left",
            "10",
            "--window-top",
            "20",
        ],
        run_browser_host=run_browser_host,
    )

    assert result == 0
    config = called_configs[0]
    assert config.endpoint.browser_host == "192.0.2.10"
    assert config.endpoint.client_host == "127.0.0.1"
    assert config.endpoint.remote_port == 13000
    assert config.browser.viewport_height == 1080
    assert config.browser.headless is False
    assert config.browser.user_data_dir == tmp_path / "user-data"
    assert config.browser.window_left == 10
    assert config.browser.window_top == 20


def test_browser_cli_propagates_browser_runner_error() -> None:
    async def run_browser_host(_config: AppConfig) -> None:
        msg = "synthetic browser startup failure"
        raise RuntimeError(msg)

    with pytest.raises(
        RuntimeError, match="synthetic browser startup failure"
    ):
        main([], run_browser_host=run_browser_host)


def test_browser_cli_does_not_run_browser_with_invalid_override() -> None:
    called = False

    async def run_browser_host(_config: AppConfig) -> None:
        nonlocal called
        called = True

    with pytest.raises(ValidationError, match="remote_port"):
        main(
            ["--remote-port", "1023"],
            run_browser_host=run_browser_host,
        )

    assert not called


def test_browser_cli_prints_version_and_exits_successfully(
    capsys: pytest.CaptureFixture[str],
) -> None:
    called = False

    async def run_browser_host(_config: AppConfig) -> None:
        nonlocal called
        called = True

    with pytest.raises(SystemExit) as exc_info:
        main(["--version"], run_browser_host=run_browser_host)

    assert exc_info.value.code == 0
    assert capsys.readouterr().out == f"majsoulrpa-browser {__version__}\n"
    assert not called


def test_browser_cli_handles_keyboard_interrupt_without_traceback() -> None:
    async def run_browser_host(_config) -> None:  # noqa: ANN001
        raise KeyboardInterrupt

    assert main([], run_browser_host=run_browser_host) == 130
