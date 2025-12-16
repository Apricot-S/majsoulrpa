import asyncio
import datetime
import tomllib
from pathlib import Path
from typing import Any

from majsoulrpa import ConfigInput, RPAClient, yostar_login
from majsoulrpa.presentation.home import HomePresentation
from majsoulrpa.presentation.login import LoginPresentation
from majsoulrpa.yostar_login import YostarLogin
from majsoulrpa.yostar_login.email_repository.s3 import S3EmailRepository

rpa = RPAClient()


@rpa.on(LoginPresentation)
async def on_login(p: LoginPresentation, config: yostar_login.Config) -> Any:
    assert config.email_address is not None
    assert config.s3 is not None

    async with asyncio.timeout(30):
        await p.enter_email_address(config.email_address)

    now = datetime.datetime.now(datetime.UTC)
    repository = S3EmailRepository(config.s3)
    yostr_login = YostarLogin(repository)

    verification_code = None
    try:
        async with asyncio.timeout(180):
            verification_code = await yostr_login.fetch_code(
                config.email_address,
                now,
                cleanup=True,
            )
    except TimeoutError:
        print("Timed out while waiting for verification code.")

    if verification_code is None:
        msg = "Could not fetch verification code."
        raise RuntimeError(msg)

    async with asyncio.timeout(30):
        await p.enter_verification_code(verification_code)

    return config


@rpa.on(HomePresentation)
async def on_home(p: HomePresentation, data: Any) -> Any:
    await asyncio.sleep(5)

    async with asyncio.timeout(5):
        await p.end_rpa(close_browser=True)

    return data


async def main() -> None:
    with Path("./config.toml").open("wb") as fp:  # noqa: ASYNC230
        config_dict = tomllib.load(fp)

    config_input = ConfigInput.model_validate(config_dict["majsoulrpa"])
    client_config = config_input.build_client_config()
    yostar_login_config = [0]  # TODO: 正式な取得処理に変える

    await rpa.run(client_config, yostar_login_config)


if __name__ == "__main__":
    asyncio.run(main())
