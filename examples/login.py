# ruff: noqa: ANN401

import asyncio
from typing import Any

from majsoulrpa import RPAClient
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

    await asyncio.sleep(2)

    async with asyncio.timeout(5):
        await p.end_rpa(close_browser=True)

    return data + 1


async def main() -> None:
    config = RPAClient.Config()
    await rpa.run(config, data=0, detection_timeout=30)
    print("The RPA client has been terminated.")


if __name__ == "__main__":
    asyncio.run(main())
