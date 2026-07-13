from typing import Protocol


class VerificationCodeProvider(Protocol):
    """Obtain a Yostar verification code from a user-selected source."""

    async def fetch(self) -> str:
        """Return a current six-digit verification code."""
        ...
