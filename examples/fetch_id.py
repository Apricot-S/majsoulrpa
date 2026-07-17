import asyncio
from dataclasses import dataclass
from pathlib import Path
from typing import Any, ClassVar

from majsoulrpa import AppConfig, RPAApp
from majsoulrpa.presentation import Region
from majsoulrpa.screens.home import HomeScreen
from majsoulrpa.screens.login import LoginScreen
from majsoulrpa.sniffer import DecodedRequestResponse, Direction

FETCH_GAME_LIVE_LIST_API_NAME = ".lq.Lobby.fetchGameLiveList"
OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "game-ids"
ROOM_MENU_SCREENSHOT_PATH = (
    Path(__file__).resolve().parent / "spectating-room-menu.png"
)
MODE_MENU_SCREENSHOT_PATH = (
    Path(__file__).resolve().parent / "spectating-mode-menu.png"
)


@dataclass(frozen=True)
class RoomSelection:
    name: str
    region: Region


@dataclass(frozen=True)
class ModeSelection:
    player_count: int
    name: str
    region: Region


@dataclass(frozen=True)
class GameIDBatch:
    room: RoomSelection
    mode: ModeSelection
    game_ids: tuple[str, ...]

    @property
    def filename(self) -> str:
        return (
            f"{self.mode.player_count}-{self.mode.name}-{self.room.name}.txt"
        )


class FetchIDScreen(HomeScreen):
    WATCH_REGION = Region(left=1195, top=975, width=92, height=75)
    ROOM_MENU_REGION = Region(left=143, top=210, width=377, height=71)
    ROOMS: ClassVar[tuple[RoomSelection, ...]] = (
        RoomSelection(
            name="gold",
            region=Region(left=143, top=281, width=322, height=71),
        ),
        RoomSelection(
            name="jade",
            region=Region(left=143, top=354, width=322, height=71),
        ),
        RoomSelection(
            name="throne",
            region=Region(left=143, top=426, width=322, height=71),
        ),
    )
    MODE_MENU_REGION = Region(left=575, top=210, width=380, height=71)
    MODES: ClassVar[tuple[ModeSelection, ...]] = (
        ModeSelection(
            player_count=4,
            name="east",
            region=Region(left=575, top=281, width=325, height=71),
        ),
        ModeSelection(
            player_count=4,
            name="south",
            region=Region(left=575, top=352, width=325, height=71),
        ),
        ModeSelection(
            player_count=3,
            name="east",
            region=Region(left=575, top=424, width=325, height=71),
        ),
        ModeSelection(
            player_count=3,
            name="south",
            region=Region(left=575, top=498, width=325, height=34),
        ),
    )

    async def enter_spectating(self) -> None:
        await self.click_region(self.WATCH_REGION)
        await asyncio.sleep(2.0)

    async def fetch_ids_once(self) -> list[GameIDBatch]:
        batches: list[GameIDBatch] = []
        for room in self.ROOMS:
            await self.click_region(self.ROOM_MENU_REGION)
            await asyncio.sleep(0.5)
            await self.click_region(room.region)
            await asyncio.sleep(1.0)

            for mode in self.MODES:
                await self.click_region(self.MODE_MENU_REGION)
                await asyncio.sleep(0.5)
                self._discard_sniffer_messages()
                await self.click_region(mode.region)

                message = await self._wait_for_sniffer_message(
                    {FETCH_GAME_LIVE_LIST_API_NAME},
                )
                batches.append(
                    GameIDBatch(
                        room=room,
                        mode=mode,
                        game_ids=tuple(self._extract_game_ids(message)),
                    ),
                )

                await asyncio.sleep(1.0)

        return batches

    @staticmethod
    def _extract_game_ids(message: object) -> list[str]:
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

        game_ids: list[str] = []
        for game_live in live_list:
            if not isinstance(game_live, dict):
                msg = "fetchGameLiveList live_list item must be an object."
                raise RuntimeError(msg)
            game_id = game_live.get("uuid")
            if not isinstance(game_id, str) or not game_id:
                msg = "fetchGameLiveList live_list item has no UUID."
                raise RuntimeError(msg)
            game_ids.append(game_id)
        return game_ids


def append_game_ids(
    batch: GameIDBatch,
    output_directory: Path = OUTPUT_DIRECTORY,
) -> Path:
    output_directory.mkdir(parents=True, exist_ok=True)
    output_path = output_directory / batch.filename
    with output_path.open("a", encoding="utf-8", newline="\n") as file:
        file.writelines(f"{game_id}\n" for game_id in batch.game_ids)
    return output_path


async def fetch_another_round() -> bool:
    while True:
        answer = (
            await asyncio.to_thread(input, "Fetch another round? [y/N]: ")
        ).strip()
        if answer in {"y", "Y"}:
            return True
        if answer in {"", "n", "N"}:
            return False
        print("Please answer y or N.")


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
async def fetch_id(screen: FetchIDScreen, data: Any) -> list[Path]:
    _ = data
    async with asyncio.timeout(30.0):
        await screen.enter_spectating()
        await screen.click_region(screen.ROOM_MENU_REGION)
        await asyncio.sleep(2.0)
        room_menu_screenshot = await screen.screenshot()
        await asyncio.to_thread(
            ROOM_MENU_SCREENSHOT_PATH.write_bytes,
            room_menu_screenshot,
        )
        print(f"Saved: {ROOM_MENU_SCREENSHOT_PATH}")

        await screen.click_region(screen.MODE_MENU_REGION)
        await asyncio.sleep(2.0)
        mode_menu_screenshot = await screen.screenshot()
        await asyncio.to_thread(
            MODE_MENU_SCREENSHOT_PATH.write_bytes,
            mode_menu_screenshot,
        )
        print(f"Saved: {MODE_MENU_SCREENSHOT_PATH}")

    await screen.stop_browser_host()
    await screen.stop_rpa()
    return [ROOM_MENU_SCREENSHOT_PATH, MODE_MENU_SCREENSHOT_PATH]


async def main() -> None:
    # Start `majsoulrpa-browser` in another terminal after this client
    # has begun waiting for the browser host.
    await rpa.run(AppConfig(), None, detection_timeout=60.0)


if __name__ == "__main__":
    asyncio.run(main())
