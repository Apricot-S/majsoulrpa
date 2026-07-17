import asyncio
import re
from pathlib import Path
from typing import Any, override

from majsoulrpa import AppConfig, RPAApp
from majsoulrpa.screens.home import HomeScreen
from majsoulrpa.screens.login import LoginScreen
from majsoulrpa.sniffer import DecodedRequestResponse

FETCH_GAME_RECORD_API_NAME = ".lq.Lobby.fetchGameRecord"
LOG_ID_PATTERN = re.compile(r"[A-Za-z0-9_-]+")
OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "game-records"


class FetchLogScreen(HomeScreen):
    @override
    async def before_callback(self) -> None:
        # This example only fetches game records. Skip HomeScreen's
        # announcement and daily-login-bonus handling so temporary
        # event dialogs cannot prevent the crawler from starting.
        pass

    async def fetch_log(
        self,
        log_id: str,
        output_directory: Path = OUTPUT_DIRECTORY,
    ) -> Path:
        if LOG_ID_PATTERN.fullmatch(log_id) is None:
            msg = "Log ID must contain only ASCII letters, digits, '_' or '-'."
            raise ValueError(msg)

        await self.goto_log(log_id)
        message = await self._wait_for_sniffer_message(
            {FETCH_GAME_RECORD_API_NAME},
        )
        if not isinstance(message, DecodedRequestResponse):
            msg = "fetchGameRecord did not produce a request/response message."
            raise RuntimeError(msg)

        await asyncio.to_thread(
            output_directory.mkdir,
            parents=True,
            exist_ok=True,
        )
        output_path = output_directory / f"{log_id}.bin"
        await asyncio.to_thread(output_path.write_bytes, message.raw.response)
        return output_path


rpa = RPAApp()


@rpa.on(LoginScreen)
async def login(screen: LoginScreen, data: Any) -> Any:
    email_address = await asyncio.to_thread(input, "Email address: ")
    async with asyncio.timeout(30.0):
        await screen.enter_email_address(email_address)

    verification_code = await asyncio.to_thread(input, "Verification code: ")
    async with asyncio.timeout(30.0):
        await screen.enter_verification_code(verification_code)

    return data


@rpa.on(FetchLogScreen)
async def fetch_log(screen: FetchLogScreen, data: Any) -> list[Path]:
    _ = data
    output_paths: list[Path] = []
    while True:
        log_id = (
            await asyncio.to_thread(input, "Log ID (blank to end): ")
        ).strip()
        if not log_id:
            break

        async with asyncio.timeout(60.0):
            output_path = await screen.fetch_log(log_id)
        output_paths.append(output_path)
        print(f"Saved: {output_path}")

    await screen.stop_browser_host()
    await screen.stop_rpa()
    return output_paths


async def main() -> None:
    # Start `majsoulrpa-browser` in another terminal after this client
    # has begun waiting for the browser host.
    await rpa.run(AppConfig(), None, detection_timeout=60.0)


if __name__ == "__main__":
    asyncio.run(main())
