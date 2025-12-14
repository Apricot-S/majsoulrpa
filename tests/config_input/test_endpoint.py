import pytest
from pydantic import ValidationError

from majsoulrpa import constants
from majsoulrpa.config_input.endpoint import Endpoint


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("browser_address", constants.DEFAULT_BROWSER_ADDRESS),
        ("client_address", constants.DEFAULT_CLIENT_ADDRESS),
        ("remote_port", constants.DEFAULT_REMOTE_PORT),
        ("sniffer_port", constants.DEFAULT_SNIFFER_PORT),
        ("proxy_port", constants.DEFAULT_PROXY_PORT),
    ],
)
def test_defaults(field: str, expected: str) -> None:
    endpoint = Endpoint.model_validate({})
    assert getattr(endpoint, field) == expected


@pytest.mark.parametrize("browser_address", ["127.0.0.2", ""])
def test_browser_address_from_dict(browser_address: str) -> None:
    endpoint = Endpoint.model_validate({"browser-address": browser_address})
    assert endpoint.browser_address == browser_address


@pytest.mark.parametrize("client_address", ["127.0.0.2", ""])
def test_client_address_from_dict(client_address: str) -> None:
    endpoint = Endpoint.model_validate({"client-address": client_address})
    assert endpoint.client_address == client_address


@pytest.mark.parametrize("remote_port", [19223, 0, -1])
def test_remote_port_from_dict(remote_port: int) -> None:
    endpoint = Endpoint.model_validate({"remote-port": remote_port})
    assert endpoint.remote_port == remote_port


@pytest.mark.parametrize("sniffer_port", [37248, 0, -1])
def test_sniffer_port_from_dict(sniffer_port: int) -> None:
    endpoint = Endpoint.model_validate({"sniffer-port": sniffer_port})
    assert endpoint.sniffer_port == sniffer_port


@pytest.mark.parametrize("proxy_port", [8081, 0, -1])
def test_proxy_port_from_dict(proxy_port: int) -> None:
    endpoint = Endpoint.model_validate({"proxy-port": proxy_port})
    assert endpoint.proxy_port == proxy_port


def test_snake_case_key_error() -> None:
    with pytest.raises(ValidationError):
        Endpoint.model_validate({"browser_address": "127.0.0.2"})


def test_remote_port_type_error() -> None:
    with pytest.raises(ValidationError):
        Endpoint.model_validate({"remote-port": "not-an-int"})
