from typing import Protocol


class VerificationCodeProvider(Protocol):
    """Structural interface for a user-selected code source.

    Implement both async methods; inheriting this Protocol is optional.
    """

    async def fetch(self, *, delete_read_emails: bool = False) -> str:
        """Wait for a code; delete emails only when requested."""
        ...

    async def fetch_nowait(self, *, delete_read_emails: bool = False) -> str:
        """Check once without polling; optionally delete emails read."""
        ...
