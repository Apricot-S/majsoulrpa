class YostarVerificationEmailError(Exception):
    """Base exception for Yostar verification email processing."""


class InvalidYostarVerificationEmailError(YostarVerificationEmailError):
    """A message is not a current Yostar verification email."""
