import asyncio
from random import Random
from typing import Any

from majsoulrpa import AppConfig, RPAApp
from majsoulrpa.screens.home import HomeScreen, Length
from majsoulrpa.screens.login import LoginScreen
from majsoulrpa.screens.match import MatchScreen
from majsoulrpa.screens.room import RoomScreen

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


@rpa.on(HomeScreen)
async def home(screen: HomeScreen, data: int) -> int:
    if data < 1:
        data += 1
        await screen.create_room(length=Length.ONE_GAME)
    else:
        await screen.stop_browser_host()
        await screen.stop_rpa()
    return data


@rpa.on(RoomScreen)
async def room(screen: RoomScreen, data: int) -> int:
    state = await screen.get_state()
    while state.available_slots > 0:
        state = await screen.add_ai()

    if await asyncio.to_thread(input, "Start match? [y/N]: ") == "y":
        await screen.start_match()
        return data

    await screen.leave()
    return data


@rpa.on(MatchScreen)
async def match(screen: MatchScreen, data: int) -> int:
    rng = Random()
    state = await screen.get_state()

    while state is not None:
        candidates = state.round.operation_candidates
        if candidates is None:
            state = await screen.wait_for_state_change(state)
            continue
        state = await screen.operate(rng.choice(candidates.operations))

    return data


async def main() -> None:
    # Start `majsoulrpa-browser` in another terminal after this client
    # has begun waiting for the browser host.
    await rpa.run(AppConfig(), 0, detection_timeout=60.0)


if __name__ == "__main__":
    asyncio.run(main())
