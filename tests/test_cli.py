from pathlib import Path

from majsoulrpa.cli import main


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
            "--browser-host",
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
    assert config.endpoint.browser_host == "127.0.0.1"
    assert config.endpoint.remote_port == 13000
    assert config.browser.viewport_height == 1080
    assert config.browser.headless is False
    assert config.browser.user_data_dir == tmp_path / "user-data"
    assert config.browser.window_left == 10
    assert config.browser.window_top == 20
