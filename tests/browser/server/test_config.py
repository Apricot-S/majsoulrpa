from ipaddress import IPv4Address, IPv6Address

import pytest

from majsoulrpa.browser.server.config import Config
from majsoulrpa.exceptions import UserInputError


def make_config(
    *,
    client_address: IPv4Address | IPv6Address | None = None,
    remote_port: int = 19222,
    sniffer_port: int = 37247,
    proxy_port: int = 8080,
) -> Config:
    return Config(
        client_address=client_address or IPv4Address("127.0.0.1"),
        remote_port=remote_port,
        sniffer_port=sniffer_port,
        proxy_port=proxy_port,
    )


@pytest.mark.parametrize("remote_port", [19222, 1024, 49151])
def test_config_init_with_valid_remote_port(remote_port: int) -> None:
    cfg = make_config(remote_port=remote_port)
    assert cfg.remote_port == remote_port


@pytest.mark.parametrize("remote_port", [1023, 49152, 0, -1024])
def test_config_init_with_invalid_remote_port(remote_port: int) -> None:
    with pytest.raises(UserInputError):
        make_config(remote_port=remote_port)


@pytest.mark.parametrize("sniffer_port", [37247, 1024, 49151])
def test_config_init_with_valid_sniffer_port(sniffer_port: int) -> None:
    cfg = make_config(sniffer_port=sniffer_port)
    assert cfg.sniffer_port == sniffer_port


@pytest.mark.parametrize("sniffer_port", [1023, 49152, 0, -1024])
def test_config_init_with_invalid_sniffer_port(sniffer_port: int) -> None:
    with pytest.raises(UserInputError):
        make_config(sniffer_port=sniffer_port)


@pytest.mark.parametrize("proxy_port", [8080, 1024, 49151])
def test_config_init_with_valid_proxy_port(proxy_port: int) -> None:
    cfg = make_config(proxy_port=proxy_port)
    assert cfg.proxy_port == proxy_port


@pytest.mark.parametrize("proxy_port", [1023, 49152, 0, -1024])
def test_config_init_with_invalid_proxy_port(proxy_port: int) -> None:
    with pytest.raises(UserInputError):
        make_config(proxy_port=proxy_port)


@pytest.mark.parametrize(
    ("remote_port", "sniffer_port", "proxy_port"),
    [
        (8000, 8000, 9000),
        (8000, 9000, 8000),
        (8000, 9000, 9000),
        (8080, 8080, 8080),
    ],
)
def test_config_init_with_port_conflict(
    remote_port: int,
    sniffer_port: int,
    proxy_port: int,
) -> None:
    with pytest.raises(UserInputError):
        make_config(
            remote_port=remote_port,
            sniffer_port=sniffer_port,
            proxy_port=proxy_port,
        )
