import asyncio

import pytest

from majsoulrpa.yostar_email import VerificationCodeProvider


class UserCodeProvider:
    """A structurally compatible implementation without inheritance."""

    def __init__(self) -> None:
        self.calls: list[tuple[str, bool]] = []

    async def fetch(self, *, delete_read_emails: bool = False) -> str:
        self.calls.append(("fetch", delete_read_emails))
        return "012345"

    async def fetch_nowait(self, *, delete_read_emails: bool = False) -> str:
        self.calls.append(("fetch_nowait", delete_read_emails))
        return "654321"


async def _obtain_codes(
    provider: VerificationCodeProvider,
    *,
    request_deletion: bool,
) -> tuple[str, str]:
    if request_deletion:
        return (
            await provider.fetch(delete_read_emails=True),
            await provider.fetch_nowait(delete_read_emails=True),
        )
    return await provider.fetch(), await provider.fetch_nowait()


@pytest.mark.parametrize(
    "request_deletion",
    [
        pytest.param(False, id="deletion-option-omitted"),
        pytest.param(True, id="deletion-explicitly-requested"),
    ],
)
def test_custom_provider_supports_typed_consumer(
    *,
    request_deletion: bool,
) -> None:
    provider = UserCodeProvider()

    result = asyncio.run(
        _obtain_codes(provider, request_deletion=request_deletion)
    )

    assert result == ("012345", "654321")
    assert provider.calls == [
        ("fetch", request_deletion),
        ("fetch_nowait", request_deletion),
    ]
