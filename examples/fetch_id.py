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
    ROOM_MENU_REGION = Region(left=153, top=220, width=357, height=51)
    ROOMS: ClassVar[tuple[RoomSelection, ...]] = (
        RoomSelection(
            name="gold",
            region=Region(left=153, top=291, width=302, height=51),
        ),
        RoomSelection(
            name="jade",
            region=Region(left=153, top=365, width=302, height=49),
        ),
        RoomSelection(
            name="throne",
            region=Region(left=153, top=437, width=302, height=48),
        ),
    )
    MODE_MENU_REGION = Region(left=585, top=220, width=360, height=51)
    MODES: ClassVar[tuple[ModeSelection, ...]] = (
        ModeSelection(
            player_count=4,
            name="east",
            region=Region(left=585, top=291, width=305, height=50),
        ),
        ModeSelection(
            player_count=4,
            name="south",
            region=Region(left=585, top=363, width=305, height=50),
        ),
        ModeSelection(
            player_count=3,
            name="east",
            region=Region(left=585, top=435, width=305, height=50),
        ),
        ModeSelection(
            player_count=3,
            name="south",
            region=Region(left=585, top=507, width=305, height=14),
        ),
    )

    async def enter_spectating(self) -> None:
        await self.click_region(self.WATCH_REGION)
        await asyncio.sleep(1.0)

    async def fetch_ids_once(self) -> list[GameIDBatch]:
        batches: list[GameIDBatch] = []
        for room in self.ROOMS:
            await self.click_region(self.ROOM_MENU_REGION)
            await asyncio.sleep(0.5)
            await self.click_region(room.region)
            await asyncio.sleep(0.5)

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

                await asyncio.sleep(0.5)

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


async def fetch_again() -> bool:
    while True:
        answer = (
            await asyncio.to_thread(input, "Fetch again? [y/N]: ")
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
    output_paths: list[Path] = []
    async with asyncio.timeout(30.0):
        await screen.enter_spectating()

    while True:
        async with asyncio.timeout(180.0):
            batches = await screen.fetch_ids_once()

        for batch in batches:
            print(f"[{batch.filename}]")
            for game_id in batch.game_ids:
                print(game_id)
            output_path = await asyncio.to_thread(append_game_ids, batch)
            output_paths.append(output_path)
            print(f"Appended: {output_path}")

        if not await fetch_again():
            break

    await screen.stop_browser_host()
    await screen.stop_rpa()
    return output_paths


async def main() -> None:
    # Start `majsoulrpa-browser` in another terminal after this client
    # has begun waiting for the browser host.
    await rpa.run(AppConfig(), None, detection_timeout=60.0)


if __name__ == "__main__":
    asyncio.run(main())
