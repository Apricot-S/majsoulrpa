import datetime
from unittest.mock import MagicMock, patch

import pytest

from majsoulrpa._impl.template import Template
from majsoulrpa.presentation.auth import (
    _MAX_EMAIL_ADDRESS_LENGTH,
    AuthPresentation,
)
from majsoulrpa.presentation.exceptions import (
    InvalidOperationError,
    PresentationNotDetectedError,
)


class DummyAuthPresentation(AuthPresentation):
    def __init__(self) -> None:
        self._mock_browser = MagicMock()
        self._new_presentation = None
        self._entered_email_address = False
        self._last_request_time: datetime.datetime | None = None

    @property
    def _browser(self) -> MagicMock:
        return self._mock_browser


def test_auth_screen_detected() -> None:
    mock_template = MagicMock()
    mock_template.match.return_value = True

    with patch.object(Template, "open_file", return_value=mock_template):
        try:
            AuthPresentation(MagicMock(), MagicMock(), MagicMock())
        except PresentationNotDetectedError:
            pytest.fail("PresentationNotDetectedError raised unexpectedly")


def test_auth_screen_not_detected() -> None:
    mock_template = MagicMock()
    mock_template.match.return_value = False

    with (
        patch.object(Template, "open_file", return_value=mock_template),
        pytest.raises(PresentationNotDetectedError),
    ):
        AuthPresentation(MagicMock(), MagicMock(), MagicMock())


def test_enter_email_address_too_long() -> None:
    presentation = DummyAuthPresentation()
    email_address = "123456789_123456789_123456789_123456789_123456789_A"
    error_msg = (
        "Keep your email address "
        f"within {_MAX_EMAIL_ADDRESS_LENGTH} characters."
    )

    with (
        patch.object(Template, "open_file"),
        pytest.raises(ValueError, match=error_msg),
    ):
        presentation.enter_email_address(email_address)

    assert not presentation._entered_email_address


def test_enter_email_address_unavailable() -> None:
    presentation = DummyAuthPresentation()
    email_address = "unavailable_email_address"
    error_msg = "This email address is unavailable."

    with (
        patch.object(Template, "open_file"),
        pytest.raises(ValueError, match=error_msg),
    ):
        presentation.enter_email_address(email_address)

    assert not presentation._entered_email_address


def test_enter_email_address_success() -> None:
    presentation = DummyAuthPresentation()
    email_address = "email_address"

    mock_template = MagicMock()
    mock_template.match.return_value = False

    with patch.object(Template, "open_file", return_value=mock_template):
        presentation.enter_email_address(email_address)

    assert presentation._entered_email_address


def test_enter_email_address_resend_within_60_seconds() -> None:
    presentation = DummyAuthPresentation()
    email_address = "email_address"

    mock_template = MagicMock()
    mock_template.match.return_value = False
    mock_datetime = MagicMock(wraps=datetime.datetime)
    mock_datetime.now.side_effect = [  # Third time used in exception
        datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.UTC),
        datetime.datetime(2024, 1, 1, 0, 1, 0, tzinfo=datetime.UTC),
        datetime.datetime(2024, 1, 1, 0, 1, 0, tzinfo=datetime.UTC),
    ]

    with (
        patch.object(Template, "open_file", return_value=mock_template),
        patch("datetime.datetime", mock_datetime),
    ):
        presentation.enter_email_address(email_address)
        assert presentation._entered_email_address

        with pytest.raises(InvalidOperationError):
            presentation.enter_email_address(email_address)


def test_enter_email_address_resend_after_61_seconds() -> None:
    presentation = DummyAuthPresentation()
    email_address = "email_address"

    mock_template = MagicMock()
    mock_template.match.return_value = False
    mock_datetime = MagicMock(wraps=datetime.datetime)
    mock_datetime.now.side_effect = [
        datetime.datetime(2024, 1, 1, 0, 0, 0, tzinfo=datetime.UTC),
        datetime.datetime(2024, 1, 1, 0, 1, 1, tzinfo=datetime.UTC),
        datetime.datetime(2024, 1, 1, 0, 1, 1, tzinfo=datetime.UTC),
    ]

    with (
        patch.object(Template, "open_file", return_value=mock_template),
        patch("datetime.datetime", mock_datetime),
    ):
        presentation.enter_email_address(email_address)
        assert presentation._entered_email_address

        try:
            presentation.enter_email_address(email_address)
        except InvalidOperationError:
            pytest.fail("InvalidOperationError raised unexpectedly")


def test_enter_auth_code_before_enter_email_address() -> None:
    presentation = DummyAuthPresentation()
    verification_code = "123456"

    with pytest.raises(InvalidOperationError):
        presentation.enter_auth_code(verification_code)


def test_enter_auth_code_incorrectly_format() -> None:
    presentation = DummyAuthPresentation()
    presentation._entered_email_address = True
    error_msg = "Verification code must be a 6-digit number."

    verification_code = ""
    with pytest.raises(ValueError, match=error_msg):
        presentation.enter_auth_code(verification_code)

    verification_code = "12345"
    with pytest.raises(ValueError, match=error_msg):
        presentation.enter_auth_code(verification_code)

    verification_code = "1234567"
    with pytest.raises(ValueError, match=error_msg):
        presentation.enter_auth_code(verification_code)

    verification_code = "12345a"
    with pytest.raises(ValueError, match=error_msg):
        presentation.enter_auth_code(verification_code)


def test_enter_auth_code_invalid() -> None:
    presentation = DummyAuthPresentation()
    presentation._entered_email_address = True
    verification_code = "123456"
    error_msg = (
        "Verification failed. Verification code may be incorrect. "
        "Please re-enter the verification code."
    )

    with (
        patch.object(Template, "open_file", return_value=MagicMock()),
        pytest.raises(ValueError, match=error_msg),
    ):
        presentation.enter_auth_code(verification_code)
