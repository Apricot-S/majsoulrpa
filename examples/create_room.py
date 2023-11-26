# ruff: noqa: INP001
import datetime
import time
from logging import INFO, StreamHandler, basicConfig, getLogger

from majsoulrpa import RPA, config
from majsoulrpa.presentation import (
    AuthPresentation,
    HomePresentation,
    LoginPresentation,
)
from majsoulrpa.yostar_login import YostarLogin

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
        if isinstance(presentation, LoginPresentation):
            presentation.login(timeout=60.0)
            if presentation.new_presentation is None:
                msg = "Could not transit to 'auth'."
                raise RuntimeError
            presentation = presentation.new_presentation
        logger.info("Login end.")

        logger.info("Auth start.")
        if isinstance(presentation, AuthPresentation):
            presentation.enter_email_address(myconfig["email_address"])

            auth_code = YostarLogin(myconfig).get_auth_code(
                start_time=login_start_time,
                timeout=20.0,
            )

            presentation.enter_auth_code(auth_code, timeout=60.0)
            if presentation.new_presentation is None:
                msg = "Could not transit to 'home'."
                raise RuntimeError
            presentation = presentation.new_presentation
        logger.info("Auth end.")

        logger.info("Home start.")
        if not isinstance(presentation, HomePresentation):
            msg = "Not transitioning to the home screen."
            raise TypeError(msg)
        log = f"account_id: {rpa.get_account_id()}"
        logger.info(log)
        presentation.create_room()

        time.sleep(7.0)

    logger.info("RPA close.")
    logger.info("program end.")
