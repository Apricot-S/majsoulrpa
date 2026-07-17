from typing import Protocol


class VerificationCodeProvider(Protocol):
    """Obtain a Yostar verification code from a user-selected source."""

    async def fetch(self, *, delete_read_emails: bool = False) -> str:
        """Wait for a code; optionally delete matching emails read."""
        ...

    async def fetch_nowait(
        self,
        *,
        delete_read_emails: bool = False,
    ) -> str:
        """Fetch once and optionally delete matching emails read."""
        ...
