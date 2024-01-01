# ruff: noqa: INP001, T201, TRY004, S101
import datetime
import time
from logging import INFO, StreamHandler, basicConfig, getLogger

from majsoulrpa import RPA, config
from majsoulrpa.presentation import (
    AuthPresentation,
    HomePresentation,
    LoginPresentation,
)
from majsoulrpa.yostar_login import YostarLoginIMAP

LOG_LEVEL = INFO
stream_handler = StreamHandler()
stream_handler.setLevel(LOG_LEVEL)
basicConfig(level=LOG_LEVEL, handlers=[stream_handler])
logger = getLogger()

if __name__ == "__main__":
    logger.info("program start.")
    myconfig = config.get_config("examples/config.toml")
    login_imap = YostarLoginIMAP(myconfig)

    with RPA(
        initial_left=myconfig["browser"]["initial_position"]["left"],
        initial_top=myconfig["browser"]["initial_position"]["top"],
        viewport_height=myconfig["browser"]["viewport_height"],
    ) as rpa:
        logger.info("RPA start.")
        presentation = rpa.wait(timeout=20.0)

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

        auth_start_time = datetime.datetime.now(datetime.UTC)
        presentation.enter_email_address(login_imap.get_email_address())
        auth_code = login_imap.get_auth_code(start_time=auth_start_time)

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

        time.sleep(15.0)

    logger.info("RPA close.")
    logger.info("program end.")
