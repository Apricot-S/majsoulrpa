class YostarVerificationEmailError(Exception):
    """Base email error; catching this alone does not justify retry."""


class InvalidYostarVerificationEmailError(YostarVerificationEmailError):
    """Invalid email; retry will not make the same message valid."""
