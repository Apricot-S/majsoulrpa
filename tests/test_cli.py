from pathlib import Path

import pytest

from majsoulrpa.cli import CommandLineArgs, get_command_line_args


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["majsoulrpa-browser"], CommandLineArgs()),
        (
            ["majsoulrpa-browser", "--client-address", "no-check"],
            CommandLineArgs(client_address="no-check"),
        ),
        (
            ["majsoulrpa-browser", "--remote-port", "-100"],
            CommandLineArgs(remote_port=-100),
        ),
        (
            ["majsoulrpa-browser", "--sniffer-port", "-100"],
            CommandLineArgs(sniffer_port=-100),
        ),
        (
            ["majsoulrpa-browser", "--proxy-port", "-200"],
            CommandLineArgs(proxy_port=-200),
        ),
        (
            ["majsoulrpa-browser", "--window-left", "-1500"],
            CommandLineArgs(window_left=-1500),
        ),
        (
            ["majsoulrpa-browser", "--window-top", "50"],
            CommandLineArgs(window_top=50),
        ),
        (
            ["majsoulrpa-browser", "--viewport-height", "720"],
            CommandLineArgs(viewport_height=720),
        ),
        (
            ["majsoulrpa-browser", "--headless"],
            CommandLineArgs(headless=True),
        ),
        (
            ["majsoulrpa-browser", "--user-data-dir", "./profile"],
            CommandLineArgs(user_data_dir=Path("./profile")),
        ),
        (
            ["majsoulrpa-browser", "--user-data-dir", "??no-check"],
            CommandLineArgs(user_data_dir=Path("??no-check")),
        ),
    ],
)
def test_get_command_line_args_set_args(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
    expected: CommandLineArgs,
) -> None:
    with monkeypatch.context() as m:
        m.setattr("sys.argv", argv)
        actual = get_command_line_args()

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
def test_get_command_line_args_invalid_args(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
) -> None:
    with monkeypatch.context() as m:
        m.setattr("sys.argv", argv)

        with pytest.raises(SystemExit):
            get_command_line_args()
