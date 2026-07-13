from typing import Protocol


class VerificationCodeProvider(Protocol):
    """Obtain a Yostar verification code from a user-selected source."""

    async def fetch(self) -> str:
        """Wait for and return a current six-digit verification code."""
        ...

    async def fetch_nowait(self) -> str:
        """Return an available code without waiting for arrival."""
        ...
