# ruff: noqa: INP001, T201, TRY004, S101
import datetime
import time
from logging import WARNING, StreamHandler, basicConfig, getLogger

from majsoulrpa import RPA, config
from majsoulrpa.presentation import (
    AuthPresentation,
    HomePresentation,
    LoginPresentation,
    RoomOwnerPresentation,
)
from majsoulrpa.presentation.match import MatchPresentation
from majsoulrpa.presentation.match.operation import (
    BabeiOperation,
    DapaiOperation,
)

LOG_LEVEL = WARNING
stream_handler = StreamHandler()
stream_handler.setLevel(LOG_LEVEL)
basicConfig(level=LOG_LEVEL, handlers=[stream_handler])
logger = getLogger()

if __name__ == "__main__":
    logger.info("program start.")
    myconfig = config.get_config("examples/config.toml")

    with RPA(
        initial_left=myconfig["initial_position"]["left"],
        initial_top=myconfig["initial_position"]["top"],
        viewport_height=myconfig["viewport_height"],
    ) as rpa:

        logger.info("RPA start.")
        presentation = rpa.wait(timeout=20.0)

        login_start_time = datetime.datetime.now(datetime.UTC)
        logger.info("Login start.")
        if not isinstance(presentation, LoginPresentation):
            msg = "Could not transit to 'login'."
            raise RuntimeError(msg)
        presentation.login(timeout=60.0)
        if presentation.new_presentation is None:
            msg = "Could not transit to 'auth'."
            raise RuntimeError(msg)
        presentation = presentation.new_presentation
        logger.info("Login end.")

        logger.info("Auth start.")
        if not isinstance(presentation, AuthPresentation):
            msg = "Could not transit to 'auth'."
            raise RuntimeError(msg)
        presentation.enter_email_address(myconfig["email_address"])
        auth_code = input("verification code: ")
        presentation.enter_auth_code(auth_code, timeout=60.0)
        if presentation.new_presentation is None:
            msg = "Could not transit to 'home'."
            raise RuntimeError
        presentation = presentation.new_presentation
        logger.info("Auth end.")

        logger.info("Home start.")
        if not isinstance(presentation, HomePresentation):
            msg = "Could not transit to 'home"
            raise RuntimeError(msg)
        presentation.create_room(mode="3-Player", length="East Only")
        if presentation.new_presentation is None:
            msg = "Could not transit to 'room'."
            raise RuntimeError(msg)
        presentation = presentation.new_presentation
        logger.info("Home end.")

        logger.info("Room start.")
        if not isinstance(presentation, RoomOwnerPresentation):
            msg = "Could not transit to 'room'."
            raise RuntimeError(msg)
        logger.info(f"room id: {presentation.room_id}")  # noqa: G004
        while presentation.num_ais < 2:  # noqa: PLR2004
            presentation.add_ai(timeout=10.0)

        if input("Do you want to start match? y/n: ") == "y":
            presentation.start(timeout=60.0)
            if presentation.new_presentation is None:
                msg = "Could not transit to 'match'."
                raise RuntimeError(msg)
            presentation = presentation.new_presentation
            logger.info("Room end.")

            logger.info("Match start.")
            if not isinstance(presentation, MatchPresentation):
                msg = "Could not transit to 'match'."
                raise RuntimeError(msg)

            seat = None
            for i, player in enumerate(presentation.players):
                if player.account_id == rpa.get_account_id():
                    assert seat is None
                    seat = i
                print(f"{player.name} ({player.level4}, {player.character})")
            assert seat is not None
            changs = ["東", "南", "西", "北"]
            print(f"{changs[presentation.chang]}{presentation.ju + 1}局"
                f"{presentation.ben}本場 (供託{presentation.liqibang}本)")
            print(f'スコア: {",".join([str(s) for s in presentation.scores])}')
            print(f"表ドラ表示牌: {presentation.dora_indicators[0]}")
            print(f"自風: {changs[seat]}")
            print(f'手牌: {",".join(presentation.shoupai)}')
            if presentation.zimopai is not None:
                print(f"自摸牌: {presentation.zimopai}")

            while True:
                ops = presentation.operation_list
                if ops is not None:
                    op = None
                    babei = False
                    for op in ops:
                        if isinstance(op, BabeiOperation):
                            babei = True
                            break
                    if babei:
                        time.sleep(0.1)
                        presentation.select_operation(op)
                        continue

                    moqie = False
                    for op in ops:
                        if isinstance(op, DapaiOperation):
                            moqie = True
                            break
                    if moqie:
                        time.sleep(0.1)
                        presentation.select_operation(op, 13)
                    else:
                        presentation.select_operation(None)
                else:
                    presentation.wait()

                if presentation.new_presentation is not None:
                    presentation = presentation.new_presentation
                    if isinstance(presentation, MatchPresentation):
                        continue
                    assert isinstance(presentation, RoomOwnerPresentation)
                    break

        presentation.leave()

        if presentation.new_presentation is None:
            msg = "Could not transit to 'home'."
            raise RuntimeError(msg)
        presentation = presentation.new_presentation

        time.sleep(15.0)

    logger.info("RPA close.")
    logger.info("program end.")
