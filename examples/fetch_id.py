import asyncio
from typing import Any, ClassVar

from majsoulrpa import AppConfig, RPAApp
from majsoulrpa.presentation import Region
from majsoulrpa.screens.home import HomeScreen
from majsoulrpa.screens.login import LoginScreen
from majsoulrpa.sniffer import DecodedRequestResponse, Direction

FETCH_GAME_LIVE_LIST_API_NAME = ".lq.Lobby.fetchGameLiveList"


class FetchIDScreen(HomeScreen):
    WATCH_REGION = Region(left=1195, top=975, width=92, height=75)
    ROOM_MENU_REGION = Region(left=144, top=211, width=377, height=72)
    ROOM_REGIONS: ClassVar[tuple[Region, ...]] = (
        Region(left=144, top=286, width=322, height=72),  # Gold Room
        Region(left=144, top=360, width=322, height=72),  # Jade Room
        Region(left=144, top=437, width=322, height=72),  # Throne Room
    )
    MODE_MENU_REGION = Region(left=578, top=211, width=377, height=72)
    MODE_REGIONS: ClassVar[tuple[Region, ...]] = (
        Region(left=578, top=286, width=322, height=72),  # Four-player East
        Region(left=578, top=360, width=322, height=72),  # Four-player South
    )

    async def fetch_ids(self) -> list[str]:
        await self.click_region(self.WATCH_REGION)
        await asyncio.sleep(1.0)

        log_ids: list[str] = []
        seen_log_ids: set[str] = set()
        for room_region in self.ROOM_REGIONS:
            await self.click_region(self.ROOM_MENU_REGION)
            await asyncio.sleep(0.5)
            await self.click_region(room_region)
            await asyncio.sleep(1.0)

            for mode_region in self.MODE_REGIONS:
                await self.click_region(self.MODE_MENU_REGION)
                await asyncio.sleep(0.5)
                self._discard_sniffer_messages()
                await self.click_region(mode_region)

                message = await self._wait_for_sniffer_message(
                    {FETCH_GAME_LIVE_LIST_API_NAME},
                )
                for log_id in self._extract_log_ids(message):
                    if log_id in seen_log_ids:
                        continue
                    seen_log_ids.add(log_id)
                    log_ids.append(log_id)

                await asyncio.sleep(1.0)

        return log_ids

    @staticmethod
    def _extract_log_ids(message: object) -> list[str]:
        if not isinstance(message, DecodedRequestResponse):
            msg = "fetchGameLiveList did not produce a Req/Res message."
            raise RuntimeError(msg)
        if message.raw.request_direction is not Direction.OUTBOUND:
            msg = "fetchGameLiveList request was not outbound."
            raise RuntimeError(msg)

        response = message.response
        if "error" in response:
            msg = "fetchGameLiveList returned an error."
            raise RuntimeError(msg)

        live_list = response.get("live_list")
        if not isinstance(live_list, list):
            msg = "fetchGameLiveList response has no live_list."
            raise RuntimeError(msg)

        log_ids: list[str] = []
        for game_live in live_list:
            if not isinstance(game_live, dict):
                msg = "fetchGameLiveList live_list item must be an object."
                raise RuntimeError(msg)
            log_id = game_live.get("uuid")
            if not isinstance(log_id, str) or not log_id:
                msg = "fetchGameLiveList live_list item has no UUID."
                raise RuntimeError(msg)
            log_ids.append(log_id)
        return log_ids


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


@rpa.on(FetchIDScreen)
async def fetch_id(screen: FetchIDScreen, data: Any) -> list[str]:
    _ = data
    async with asyncio.timeout(180.0):
        log_ids = await screen.fetch_ids()

    for log_id in log_ids:
        print(log_id)

    await screen.stop_browser_host()
    await screen.stop_rpa()
    return log_ids


async def main() -> None:
    # Start `majsoulrpa-browser` in another terminal after this client
    # has begun waiting for the browser host.
    await rpa.run(AppConfig(), None, detection_timeout=60.0)


if __name__ == "__main__":
    asyncio.run(main())
