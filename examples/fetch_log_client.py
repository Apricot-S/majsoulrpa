# ruff: noqa: ANN401

import asyncio
from typing import Any

from majsoulrpa import RPAClient
from majsoulrpa.presentation.base import require_active
from majsoulrpa.presentation.home import HomePresentation
from majsoulrpa.presentation.login import LoginPresentation


class FetchLogPresentation(HomePresentation):
    @require_active
    async def fetch_log(self, log_id: str) -> None:
        await self._driver.goto_log(log_id)
        while True:
            message = await self._message_queue.get()
            if message.name == ".lq.Lobby.fetchGameRecord":
                return


rpa = RPAClient()


@rpa.on(LoginPresentation)
async def on_login(p: LoginPresentation, data: Any) -> Any:
    email_address = input("Enter your email address: ")
    async with asyncio.timeout(30):
        await p.enter_email_address(email_address)

    verification_code = input("Enter the verification code: ")
    async with asyncio.timeout(30):
        await p.enter_verification_code(verification_code)

    return data


@rpa.on(FetchLogPresentation)
async def on_home(p: FetchLogPresentation, data: Any) -> Any:
    log_id = input("Enter the log id: ")
    async with asyncio.timeout(60):
        await p.fetch_log(log_id)

    async with asyncio.timeout(5):
        await p.end_rpa(close_browser=True)

    return data


async def main() -> None:
    config = RPAClient.Config()
    await rpa.run(config, None, detection_timeout=30)


if __name__ == "__main__":
    asyncio.run(main())
