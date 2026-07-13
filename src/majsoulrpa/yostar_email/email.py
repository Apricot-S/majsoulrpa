from datetime import UTC, datetime, timedelta
from email import policy
from email.parser import BytesParser
from email.utils import getaddresses

from majsoulrpa.yostar_email.constants import (
    VERIFICATION_EMAIL_EXPIRATION,
    YOSTAR_EMAIL_ADDRESS,
    YOSTAR_EMAIL_SUBJECT_PATTERN,
)
from majsoulrpa.yostar_email.errors import (
    InvalidYostarVerificationEmailError,
)


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

    message = BytesParser(policy=policy.default).parsebytes(message_bytes)
    senders = [
        address.casefold()
        for _, address in getaddresses(message.get_all("From", []))
    ]
    if senders != [YOSTAR_EMAIL_ADDRESS]:
        msg = "The message sender is not the expected Yostar address."
        raise InvalidYostarVerificationEmailError(msg)

    recipients = {
        address.casefold()
        for _, address in getaddresses(message.get_all("To", []))
    }
    if recipient.casefold() not in recipients:
        msg = "The message recipient does not match the requested recipient."
        raise InvalidYostarVerificationEmailError(msg)

    subject = message.get("Subject")
    match = YOSTAR_EMAIL_SUBJECT_PATTERN.fullmatch(subject or "")
    if match is None:
        msg = "The message subject is not a Yostar verification subject."
        raise InvalidYostarVerificationEmailError(msg)
    return match.group("code")
