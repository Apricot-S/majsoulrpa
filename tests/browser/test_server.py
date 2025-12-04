from pathlib import Path
from typing import NoReturn

import pytest
from playwright.async_api import ViewportSize

from majsoulrpa.browser import server
from majsoulrpa.exceptions import UserInputError


@pytest.mark.parametrize(
    ("argv", "expected"),
    [
        (["majsoulrpa-browser"], server.CommandLineArgs()),
        (
            ["majsoulrpa-browser", "--client-address", "no-check"],
            server.CommandLineArgs(client_address="no-check"),
        ),
        (
            ["majsoulrpa-browser", "--remote-port", "-100"],
            server.CommandLineArgs(remote_port=-100),
        ),
        (
            ["majsoulrpa-browser", "--sniffer-port", "-100"],
            server.CommandLineArgs(sniffer_port=-100),
        ),
        (
            ["majsoulrpa-browser", "--proxy-port", "-200"],
            server.CommandLineArgs(proxy_port=-200),
        ),
        (
            ["majsoulrpa-browser", "--window-left", "-1500"],
            server.CommandLineArgs(window_left=-1500),
        ),
        (
            ["majsoulrpa-browser", "--window-top", "50"],
            server.CommandLineArgs(window_top=50),
        ),
        (
            ["majsoulrpa-browser", "--viewport-height", "720"],
            server.CommandLineArgs(viewport_height=720),
        ),
        (
            ["majsoulrpa-browser", "--headless"],
            server.CommandLineArgs(headless=True),
        ),
        (
            ["majsoulrpa-browser", "--user-data-dir", "./profile"],
            server.CommandLineArgs(user_data_dir=Path("./profile")),
        ),
        (
            ["majsoulrpa-browser", "--user-data-dir", "??no-check"],
            server.CommandLineArgs(user_data_dir=Path("??no-check")),
        ),
    ],
)
def test_get_command_line_args_set_args(
    monkeypatch: pytest.MonkeyPatch,
    argv: list[str],
    expected: server.CommandLineArgs,
) -> None:
    with monkeypatch.context() as m:
        m.setattr("sys.argv", argv)
        actual = server.get_command_line_args()

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
            server.get_command_line_args()


def test_resolve_user_data_dir_none() -> None:
    args = server.CommandLineArgs(user_data_dir=None)
    assert server.resolve_user_data_dir(args) is None


def test_resolve_user_data_dir_existing(tmp_path: Path) -> None:
    args = server.CommandLineArgs(user_data_dir=tmp_path)
    result = server.resolve_user_data_dir(args)
    assert result is not None
    assert result == tmp_path.resolve()
    assert result.exists()


def test_resolve_user_data_dir_create(tmp_path: Path) -> None:
    new_dir = tmp_path / "new_dir"
    args = server.CommandLineArgs(user_data_dir=new_dir)
    result = server.resolve_user_data_dir(args)
    assert result is not None
    assert result == new_dir.resolve()
    assert result.exists()
    assert result.is_dir()


def test_resolve_user_data_dir_file_exists(tmp_path: Path) -> None:
    file_path = tmp_path / "conflict"
    file_path.write_text("dummy")
    args = server.CommandLineArgs(user_data_dir=file_path)
    with pytest.raises(UserInputError):
        server.resolve_user_data_dir(args)


def test_resolve_user_data_dir_invalid(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path: Path,
) -> None:
    bad_path = tmp_path / "bad_dir"

    def fake_mkdir(*_args, **_kwargs) -> NoReturn:
        msg = "cannot create"
        raise OSError(msg)

    monkeypatch.setattr(Path, "mkdir", fake_mkdir)

    args = server.CommandLineArgs(user_data_dir=bad_path)
    with pytest.raises(UserInputError):
        server.resolve_user_data_dir(args)


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (
            server.CommandLineArgs(),
            [
                "--window-position=0,0",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            server.CommandLineArgs(window_left=100),
            [
                "--window-position=100,0",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            server.CommandLineArgs(window_top=-50),
            [
                "--window-position=0,-50",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            server.CommandLineArgs(window_left=-200, window_top=100),
            [
                "--window-position=-200,100",
                "--proxy-server=http://localhost:8080",
                "--ignore-certificate-errors",
            ],
        ),
        (
            server.CommandLineArgs(proxy_port=8081),
            [
                "--window-position=0,0",
                "--proxy-server=http://localhost:8081",
                "--ignore-certificate-errors",
            ],
        ),
    ],
)
def test_create_browser_args(
    args: server.CommandLineArgs,
    expected: list[str],
) -> None:
    actual = server.create_browser_args(args)
    assert actual == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (server.CommandLineArgs(headless=True), []),
        (server.CommandLineArgs(headless=False), ["--mute-audio"]),
    ],
)
def test_create_ignored_default_args(
    args: server.CommandLineArgs,
    expected: list[str],
) -> None:
    actual = server.create_ignored_default_args(args)
    assert actual == expected


@pytest.mark.parametrize(
    ("args", "expected"),
    [
        (
            server.CommandLineArgs(),
            (ViewportSize(width=1920, height=1080), 1.0),
        ),
        (
            server.CommandLineArgs(viewport_height=540),
            (ViewportSize(width=960, height=540), 0.5),
        ),
        (
            server.CommandLineArgs(viewport_height=720),
            (ViewportSize(width=1280, height=720), 2 / 3),
        ),
        (
            server.CommandLineArgs(viewport_height=900),
            (ViewportSize(width=1600, height=900), 5 / 6),
        ),
        (
            server.CommandLineArgs(viewport_height=1440),
            (ViewportSize(width=2560, height=1440), 4 / 3),
        ),
    ],
)
def test_get_viewport_size(
    args: server.CommandLineArgs,
    expected: tuple[ViewportSize, float],
) -> None:
    actual = server.get_viewport_size(args)
    assert actual == expected
