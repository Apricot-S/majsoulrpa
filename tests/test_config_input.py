import pytest

from majsoulrpa.config_input import ConfigInput
from majsoulrpa.constants import DEFAULT_BROWSER_ADDRESS


def test_browser_address_default() -> None:
    input_dict: dict = {}
    ci = ConfigInput.model_validate(input_dict)
    assert ci.browser_address == DEFAULT_BROWSER_ADDRESS


@pytest.mark.parametrize("browser_address", ["127.0.0.2", ""])
def test_browser_address_from_dict(browser_address: str) -> None:
    input_dict = {"browser-address": browser_address}
    ci = ConfigInput.model_validate(input_dict)
    assert ci.browser_address == browser_address
