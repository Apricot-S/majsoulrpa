import pytest

from majsoulrpa.presentation import exceptions
from majsoulrpa.presentation.login import validate_email_address


@pytest.mark.parametrize(
    "email_address",
    [
        "very.long.email.address.for.yostar.login.tests@example.com",
        "user+tag@example.com",
        "user_name@example-domain.co.jp",
        "!#$%&'*+/=?^_`{|}~-@example.com",
    ],
)
def test_validate_email_address_accepts_valid_address(
    email_address: str,
) -> None:
    validate_email_address(email_address)


@pytest.mark.parametrize(
    "email_address",
    [
        "",
        '"user"@example.com',
        ".user@example.com",
        "user..name@example.com",
        "user@example",
        "user@sub_domain.example.com",
        "user@example.\u307f\u3093\u306a",
        f"{'a' * 65}@example.com",
    ],
)
def test_validate_email_address_rejects_invalid_address(
    email_address: str,
) -> None:
    with pytest.raises(exceptions.InvalidArgumentError):
        validate_email_address(email_address)


def test_validate_email_address_reports_yostar_restriction() -> None:
    with pytest.raises(
        exceptions.InvalidArgumentError,
        match="not available for Yostar login",
    ):
        validate_email_address('"user"@example.com')
