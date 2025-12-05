# ruff: noqa: ANN401

import asyncio
from typing import Any

from majsoulrpa import RPAClient
from majsoulrpa.presentation.login import LoginPresentation

rpa = RPAClient()


@rpa.on(LoginPresentation)
async def on_login(
    p: LoginPresentation,
    data: Any,
) -> tuple[LoginPresentation, Any]:
    async with asyncio.timeout(30):
        await p.enter_email_address("majsoul-rpa-dev@example.com")
        await asyncio.sleep(2)
        await p.end(close_browser=True)

    return p, data + 1


async def main() -> None:
    config = RPAClient.Config("127.0.0.1", 19222)
    await rpa.run(config, data=0, detection_timeout=30)
    print("Done!!!")


if __name__ == "__main__":
    asyncio.run(main())
