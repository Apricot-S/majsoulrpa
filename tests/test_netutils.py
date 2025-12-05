from ipaddress import IPv4Address, IPv6Address

import pytest

from majsoulrpa import netutils
from majsoulrpa.exceptions import UserInputError


@pytest.mark.parametrize(
    ("raw_ip_address", "expected"),
    [
        ("192.168.0.1", IPv4Address("192.168.0.1")),
        ("2001:db8::1", IPv6Address("2001:db8::1")),
        ("127.0.0.1", IPv4Address("127.0.0.1")),
        ("::1", IPv6Address("::1")),
    ],
)
def test_parse_ip_address_valid(
    raw_ip_address: str,
    expected: IPv4Address | IPv6Address,
) -> None:
    ip = netutils.parse_ip_address(raw_ip_address)
    assert ip == expected


@pytest.mark.parametrize(
    "raw_ip_address",
    ["999.999.999.999", "2001:db8:::1", "localhost"],
)
def test_parse_ip_address_invalid(raw_ip_address: str) -> None:
    with pytest.raises(UserInputError):
        netutils.parse_ip_address(raw_ip_address)


@pytest.mark.parametrize("port", [1024, 49151, 19222])
def test_validate_user_port_valid(port: int) -> None:
    p = netutils.validate_user_port(port)
    assert p == netutils.UserPort(port)


@pytest.mark.parametrize("port", [1023, 49152, -19222])
def test_validate_user_port_invalid(port: int) -> None:
    with pytest.raises(UserInputError):
        netutils.validate_user_port(port)


@pytest.mark.parametrize(
    ("address", "port", "expected"),
    [
        (
            IPv4Address("192.168.0.1"),
            netutils.UserPort(19222),
            "192.168.0.1:19222",
        ),
        (
            IPv6Address("2001:db8::1"),
            netutils.UserPort(19222),
            "[2001:db8::1]:19222",
        ),
    ],
)
def test_make_endpoint(
    address: IPv4Address | IPv6Address,
    port: netutils.UserPort,
    expected: str,
) -> None:
    assert netutils.make_endpoint(address, port) == expected
