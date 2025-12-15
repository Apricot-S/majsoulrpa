from ipaddress import IPv4Address, IPv6Address

import pytest

from majsoulrpa.exceptions import UserInputError
from majsoulrpa.netutils import validate_user_port
from majsoulrpa.rpa_client import Config


def make_config(
    *,
    browser_address: IPv4Address | IPv6Address | None = None,
    remote_port: int = 19222,
    sniffer_port: int = 37247,
) -> Config:
    return Config(
        browser_address=browser_address or IPv4Address("127.0.0.1"),
        remote_port=validate_user_port(remote_port),
        sniffer_port=validate_user_port(sniffer_port),
    )


@pytest.mark.parametrize("remote_port", [19222, 1024, 49151])
def test_config_init_with_valid_remote_port(remote_port: int) -> None:
    cfg = make_config(remote_port=remote_port)
    assert cfg.remote_port == remote_port


@pytest.mark.parametrize("sniffer_port", [37247, 1024, 49151])
def test_config_init_with_valid_sniffer_port(sniffer_port: int) -> None:
    cfg = make_config(sniffer_port=sniffer_port)
    assert cfg.sniffer_port == sniffer_port


def test_config_init_with_port_conflict() -> None:
    with pytest.raises(UserInputError):
        make_config(remote_port=8080, sniffer_port=8080)
