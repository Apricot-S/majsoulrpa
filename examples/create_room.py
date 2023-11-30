# ruff: noqa: INP001, TRY004
import datetime
import time
from logging import INFO, StreamHandler, basicConfig, getLogger

from majsoulrpa import RPA, config
from majsoulrpa.presentation import (
    AuthPresentation,
    HomePresentation,
    LoginPresentation,
    RoomHostPresentation,
)

LOG_LEVEL = INFO
stream_handler = StreamHandler()
stream_handler.setLevel(LOG_LEVEL)
basicConfig(level=LOG_LEVEL, handlers=[stream_handler])
logger = getLogger()

if __name__ == "__main__":
    logger.info("program start.")
    myconfig = config.get_config("examples/config.toml")

    with RPA(initial_left=myconfig["initial_position"]["left"],
             initial_top=myconfig["initial_position"]["top"],
             viewport_height=myconfig["viewport_height"]) as rpa:

        logger.info("RPA start.")
        presentation = rpa.wait(timeout=20.0)

        login_start_time=datetime.datetime.now(datetime.UTC)
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
        presentation.create_room()
        if presentation.new_presentation is None:
            msg = "Could not transit to 'room'."
            raise RuntimeError(msg)
        presentation = presentation.new_presentation
        logger.info("Home end.")

        if not isinstance(presentation, RoomHostPresentation):
            msg = "Could not transit to 'room'."
            raise RuntimeError(msg)
        logger.info(f"room id: {presentation.room_id}")  # noqa: G004
        while presentation.num_ais < 3:  # noqa: PLR2004
            presentation.add_ai(timeout=10.0)
        presentation.start(timeout=60.0)

        time.sleep(30.0)

    logger.info("RPA close.")
    logger.info("program end.")
