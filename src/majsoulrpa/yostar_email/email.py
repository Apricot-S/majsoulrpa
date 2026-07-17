from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses
from typing import Self

from majsoulrpa.yostar_email.constants import (
    VERIFICATION_EMAIL_EXPIRATION,
    YOSTAR_EMAIL_ADDRESS,
    YOSTAR_EMAIL_SUBJECT_PATTERN,
)
from majsoulrpa.yostar_email.errors import (
    InvalidYostarVerificationEmailError,
)


@dataclass(frozen=True, slots=True)
class VerificationEmail:
    """Parsed fields used to classify and validate an email."""

    senders: tuple[str, ...]
    recipients: frozenset[str]
    verification_code: str | None

    @classmethod
    def parse(cls, message_bytes: bytes) -> Self:
        """Parse the MIME headers used for verification emails."""
        message = BytesParser(policy=policy.default).parsebytes(message_bytes)
        senders = tuple(
            address.casefold()
            for _, address in getaddresses(message.get_all("From", []))
        )
        recipients = frozenset(
            address.casefold()
            for _, address in getaddresses(message.get_all("To", []))
        )
        subject = message.get("Subject")
        match = YOSTAR_EMAIL_SUBJECT_PATTERN.fullmatch(subject or "")
        verification_code = None if match is None else match.group("code")
        return cls(
            senders=senders,
            recipients=recipients,
            verification_code=verification_code,
        )

    def matches_deletion_condition(self, *, recipient: str) -> bool:
        """Check the recipient and verification-email subject."""
        return (
            recipient.casefold() in self.recipients
            and self.verification_code is not None
        )

    def extract_code(self, *, recipient: str) -> str:
        """Validate the parsed fields and return the code."""
        if self.senders != (YOSTAR_EMAIL_ADDRESS,):
            msg = "The message sender is not the expected Yostar address."
            raise InvalidYostarVerificationEmailError(msg)
        if recipient.casefold() not in self.recipients:
            msg = (
                "The message recipient does not match the requested recipient."
            )
            raise InvalidYostarVerificationEmailError(msg)
        if self.verification_code is None:
            msg = "The message subject is not a Yostar verification subject."
            raise InvalidYostarVerificationEmailError(msg)
        return self.verification_code


def extract_verification_code(
    message_bytes: bytes,
    *,
    recipient: str,
    received_at: datetime,
    now: datetime | None = None,
) -> str:
    """Validate a JP Yostar email and return its verification code."""
    current_time = datetime.now(UTC) if now is None else now
    if current_time.tzinfo is None or received_at.tzinfo is None:
        msg = "Email timestamps must include timezone information."
        raise ValueError(msg)

    age = current_time - received_at
    if age < timedelta(0) or age >= VERIFICATION_EMAIL_EXPIRATION:
        msg = "The verification email is outside its validity period."
        raise InvalidYostarVerificationEmailError(msg)

    return VerificationEmail.parse(message_bytes).extract_code(
        recipient=recipient,
    )
