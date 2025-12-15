from pathlib import Path

import pytest

from majsoulrpa.cli import build_config_input_from_cli
from majsoulrpa.config_input import Browser, ConfigInput, Endpoint


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["majsoulrpa-browser"], ConfigInput()),
        (
            ["majsoulrpa-browser", "--client-address", "no-check"],
            ConfigInput(endpoint=Endpoint(client_address="no-check")),
        ),
        (
            ["majsoulrpa-browser", "--remote-port", "-100"],
            ConfigInput(endpoint=Endpoint(remote_port=-100)),
        ),
        (
            ["majsoulrpa-browser", "--sniffer-port", "-100"],
            ConfigInput(endpoint=Endpoint(sniffer_port=-100)),
        ),
        (
            ["majsoulrpa-browser", "--proxy-port", "-200"],
            ConfigInput(endpoint=Endpoint(proxy_port=-200)),
        ),
        (
            ["majsoulrpa-browser", "--window-left", "-1500"],
            ConfigInput(browser=Browser(window_left=-1500)),
        ),
        (
            ["majsoulrpa-browser", "--window-top", "50"],
            ConfigInput(browser=Browser(window_top=50)),
        ),
        (
            ["majsoulrpa-browser", "--viewport-height", "720"],
            ConfigInput(browser=Browser(viewport_height=720)),
        ),
        (
            ["majsoulrpa-browser", "--headless"],
            ConfigInput(browser=Browser(headless=True)),
        ),
        (
            ["majsoulrpa-browser", "--user-data-dir", "./profile"],
            ConfigInput(browser=Browser(user_data_dir=Path("./profile"))),
        ),
        (
            ["majsoulrpa-browser", "--user-data-dir", "??no-check"],
            ConfigInput(browser=Browser(user_data_dir=Path("??no-check"))),
        ),
    ],
)
def test_build_config_input_from_cli_set_args(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
    expected: ConfigInput,
) -> None:
    with monkeypatch.context() as m:
        m.setattr("sys.argv", argv)
        actual = build_config_input_from_cli()

    assert actual == expected


@pytest.mark.parametrize(
    "argv",
    [
        ["majsoulrpa-browser", "--remote-port", "5555.0"],
        ["majsoulrpa-browser", "--sniffer-port", "5555.0"],
        ["majsoulrpa-browser", "--proxy-port", "5555.0"],
        ["majsoulrpa-browser", "--window-left", "-1.0"],
        ["majsoulrpa-browser", "--window-top", "0.0"],
        ["majsoulrpa-browser", "--viewport-height", "1000"],
        ["majsoulrpa-browser", "--viewport-height", "720.0"],
    ],
)
def test_build_config_input_from_cli_invalid_args(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
) -> None:
    with monkeypatch.context() as m:
        m.setattr("sys.argv", argv)

        with pytest.raises(SystemExit):
            build_config_input_from_cli()
