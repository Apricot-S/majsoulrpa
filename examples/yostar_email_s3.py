import asyncio
from pathlib import Path

from majsoulrpa import AppConfig, RPAApp
from majsoulrpa.screens.home import HomeScreen
from majsoulrpa.screens.login import LoginScreen
from majsoulrpa.yostar_email.s3 import (
    S3VerificationCodeProvider,
)

EXAMPLES_DIRECTORY = Path(__file__).resolve().parent
CONFIG_PATH = EXAMPLES_DIRECTORY / "config.toml"
EMAIL_WAIT_TIMEOUT_SECONDS = 10.0 * 60.0
EMAIL_POLL_INTERVAL_SECONDS = 5.0


def create_rpa(config: AppConfig) -> RPAApp:
    if config.yostar_email is None:
        msg = "config.toml does not contain [yostar_email]."
        raise ValueError(msg)
    email_config = config.yostar_email
    s3_config = email_config.s3
    if s3_config is None:
        msg = "config.toml does not contain [yostar_email.s3]."
        raise ValueError(msg)

    rpa = RPAApp()

    @rpa.on(LoginScreen)
    async def login(screen: LoginScreen, data: None) -> None:
        _ = data
        async with asyncio.timeout(30.0):
            await screen.enter_email_address(email_config.email_address)

        code_provider = S3VerificationCodeProvider(
            email_address=email_config.email_address,
            bucket_name=s3_config.bucket_name,
            key_prefix=s3_config.key_prefix,
            aws_profile=s3_config.aws_profile,
        )
        async with asyncio.timeout(EMAIL_WAIT_TIMEOUT_SECONDS):
            verification_code = await code_provider.fetch(
                poll_interval=EMAIL_POLL_INTERVAL_SECONDS,
            )

        async with asyncio.timeout(30.0):
            await screen.enter_verification_code(verification_code)

    @rpa.on(HomeScreen)
    async def home(screen: HomeScreen, data: None) -> None:
        _ = data
        await asyncio.sleep(2.0)
        await screen.stop_browser_host()
        await screen.stop_rpa()

    return rpa


async def main() -> None:
    # Create examples/config.toml from examples/config.example.toml and
    # configure the [yostar_email] and [yostar_email.s3] sections first.
    config = AppConfig.from_toml_file(CONFIG_PATH)
    rpa = create_rpa(config)

    # After this client starts waiting, run `majsoulrpa-browser --config
    # examples/config.toml` in another terminal.
    await rpa.run(config, None, detection_timeout=60.0)


if __name__ == "__main__":
    asyncio.run(main())
