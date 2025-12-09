# ruff: noqa: ANN401

import asyncio
from typing import Any

from majsoulrpa import RPAClient
from majsoulrpa.presentation.home import HomePresentation
from majsoulrpa.presentation.login import LoginPresentation

rpa = RPAClient()


@rpa.on(LoginPresentation)
async def on_login(p: LoginPresentation, data: Any) -> Any:
    email_address = input("Enter your email address: ")
    async with asyncio.timeout(10):
        await p.enter_email_address(email_address)

    verification_code = input("Enter the verification code: ")
    async with asyncio.timeout(10):
        await p.enter_verification_code(verification_code)

    return data + 1


@rpa.on(HomePresentation)
async def on_home(p: HomePresentation, data: Any) -> Any:
    await asyncio.sleep(5)

    async with asyncio.timeout(5):
        await p.end_rpa(close_browser=True)

    return data + 1


async def main() -> None:
    config = RPAClient.Config()
    data = 0

    await rpa.run(config, data, detection_timeout=30)

    print(f"{data=}")
    print("The RPA client has been terminated.")


if __name__ == "__main__":
    asyncio.run(main())
