import base64
import binascii
import re
from dataclasses import dataclass, field
from datetime import UTC, datetime, timedelta
from email import policy
from email.errors import HeaderParseError
from email.header import decode_header
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

    senders: tuple[str, ...] = field(repr=False)
    recipients: frozenset[str] = field(repr=False)
    verification_code: str | None = field(repr=False)

    @classmethod
    def parse(cls, message_bytes: bytes) -> Self:
        """Parse the MIME headers used for verification emails."""
        message = BytesParser(policy=policy.default).parsebytes(message_bytes)
        has_structure_defects = any(part.defects for part in message.walk())

        sender_headers = message.get_all("From", [])
        valid_sender_headers = (
            sender_headers
            if len(sender_headers) == 1 and not sender_headers[0].defects
            else []
        )
        senders = tuple(
            address.casefold()
            for _, address in getaddresses(valid_sender_headers)
        )

        recipient_headers = message.get_all("To", [])
        valid_recipient_headers = (
            recipient_headers
            if len(recipient_headers) == 1 and not recipient_headers[0].defects
            else []
        )
        recipients = frozenset(
            address.casefold()
            for _, address in getaddresses(valid_recipient_headers)
        )

        subjects = message.get_all("Subject", [])
        subject = (
            subjects[0]
            if (
                not has_structure_defects
                and len(subjects) == 1
                and not subjects[0].defects
            )
            else None
        )
        if subject is not None:
            raw_subject = next(
                value
                for name, value in message.raw_items()
                if name.casefold() == "subject"
            )
            try:
                for encoded_word in re.finditer(
                    r"=\?[^?]+\?[bB]\?([^?]*)\?=", raw_subject
                ):
                    base64.b64decode(encoded_word.group(1), validate=True)
                for fragment, charset in decode_header(raw_subject):
                    if isinstance(fragment, bytes):
                        fragment.decode(charset or "ascii")
            except (
                HeaderParseError,
                LookupError,
                UnicodeError,
                binascii.Error,
            ):
                subject = None

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
    if current_time.utcoffset() is None or received_at.utcoffset() is None:
        msg = "Email timestamps must include timezone information."
        raise ValueError(msg)

    age = current_time.astimezone(UTC) - received_at.astimezone(UTC)
    if age < timedelta(0) or age >= VERIFICATION_EMAIL_EXPIRATION:
        msg = "The verification email is outside its validity period."
        raise InvalidYostarVerificationEmailError(msg)

    return VerificationEmail.parse(message_bytes).extract_code(
        recipient=recipient,
    )
