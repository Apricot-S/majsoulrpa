import pytest
from pydantic import ValidationError

from majsoulrpa import constants
from majsoulrpa.config_input.endpoint import Endpoint


@pytest.mark.parametrize(
    ("field", "expected"),
    [
        ("browser_address", constants.DEFAULT_BROWSER_ADDRESS),
        ("client_address", constants.DEFAULT_CLIENT_ADDRESS),
    ],
)
def test_defaults(field: str, expected: str) -> None:
    ci = Endpoint.model_validate({})
    assert getattr(ci, field) == expected


@pytest.mark.parametrize("browser_address", ["127.0.0.2", ""])
def test_browser_address_from_dict(browser_address: str) -> None:
    ci = Endpoint.model_validate({"browser-address": browser_address})
    assert ci.browser_address == browser_address


def test_snake_case_key_error() -> None:
    with pytest.raises(ValidationError):
        Endpoint.model_validate({"browser_address": "127.0.0.2"})
