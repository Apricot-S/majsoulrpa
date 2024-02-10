import time
from logging import WARNING, StreamHandler, basicConfig

from majsoulrpa import RPA, config
from majsoulrpa.presentation import (
    AuthPresentation,
    HomePresentation,
    LoginPresentation,
    RoomHostPresentation,
)
from majsoulrpa.presentation.match import MatchPresentation
from majsoulrpa.presentation.match.operation import (
    DapaiOperation,
    LiqiOperation,
    OperationBase,
)

LOG_LEVEL = WARNING
stream_handler = StreamHandler()
stream_handler.setLevel(LOG_LEVEL)
basicConfig(level=LOG_LEVEL, handlers=[stream_handler])

if __name__ == "__main__":
    my_config = config.get_config("examples/config.toml")

    with RPA.from_config(my_config) as rpa:
        presentation = rpa.wait(timeout=20.0)

        if not isinstance(presentation, HomePresentation):
            if not isinstance(presentation, LoginPresentation):
                msg = "Could not transit to `login`."
                raise RuntimeError(msg)
            presentation.login(timeout=60.0)
            if presentation.new_presentation is None:
                msg = "Could not transit to `auth`."
                raise RuntimeError(msg)
            presentation = presentation.new_presentation

            if not isinstance(presentation, AuthPresentation):
                msg = "Could not transit to `auth`."
                raise RuntimeError(msg)
            presentation.enter_email_address(
                my_config["authentication"]["email_address"],
            )
            auth_code = input("verification code: ")
            presentation.enter_auth_code(auth_code, timeout=60.0)
            if presentation.new_presentation is None:
                msg = "Could not transit to `home`."
                raise RuntimeError
            presentation = presentation.new_presentation

        if not isinstance(presentation, HomePresentation):
            msg = "Could not transit to `home`."
            raise RuntimeError(msg)
        presentation.create_room(mode="3-Player", length="East Only")
        if presentation.new_presentation is None:
            msg = "Could not transit to `room`."
            raise RuntimeError(msg)
        presentation = presentation.new_presentation

        if not isinstance(presentation, RoomHostPresentation):
            msg = "Could not transit to `room`."
            raise RuntimeError(msg)
        print(f"room id: {presentation.room_id}")
        while presentation.num_ais < 2:  # noqa: PLR2004
            presentation.add_ai(timeout=10.0)

        if input("Do you want to start match? y/n: ") == "y":
            presentation.start(timeout=60.0)
            if presentation.new_presentation is None:
                msg = "Could not transit to `match`."
                raise RuntimeError(msg)
            presentation = presentation.new_presentation

            if not isinstance(presentation, MatchPresentation):
                msg = "Could not transit to `match`."
                raise RuntimeError(msg)

            seat = None
            for i, player in enumerate(presentation.players):
                if player.account_id == rpa.get_account_id():
                    assert seat is None
                    seat = i
                print(f"{player.name} ({player.level3}, {player.character})")
            assert seat is not None
            changs = ["東", "南", "西", "北"]
            print(
                f"{changs[presentation.chang]}{presentation.ju + 1}局"
                f"{presentation.ben}本場 (供託{presentation.liqibang}本)",
            )
            print(f"スコア: {','.join([str(s) for s in presentation.scores])}")
            print(f"表ドラ表示牌: {presentation.dora_indicators[0]}")
            print(f"自風: {changs[seat]}")
            print(f"手牌: {','.join(presentation.shoupai)}")
            if presentation.zimopai is not None:
                print(f"自摸牌: {presentation.zimopai}")

            while True:
                ops = presentation.operation_list
                if ops is not None:
                    liqi_operation: OperationBase | None = None
                    dapai_operation: OperationBase | None = None

                    can_liqi = False
                    for op in ops:
                        if isinstance(op, LiqiOperation):
                            can_liqi = True
                            liqi_operation = op
                            break

                    can_dapai = False
                    for op in ops:
                        if isinstance(op, DapaiOperation):
                            can_dapai = True
                            dapai_operation = op
                            break

                    if can_liqi:
                        index = int(input("index of liqi dapai: "))
                        presentation.select_operation(liqi_operation, index)
                    elif can_dapai:
                        index = int(input("index of dapai: "))
                        presentation.select_operation(dapai_operation, index)
                    else:
                        presentation.select_operation(None)
                else:
                    presentation.wait()

                if presentation.new_presentation is not None:
                    presentation = presentation.new_presentation
                    if isinstance(presentation, MatchPresentation):
                        continue
                    assert isinstance(presentation, RoomHostPresentation)
                    break

        presentation.leave()

        if presentation.new_presentation is None:
            msg = "Could not transit to `home`."
            raise RuntimeError(msg)
        presentation = presentation.new_presentation

        time.sleep(5.0)
