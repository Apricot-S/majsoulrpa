import datetime
import time
from logging import INFO, StreamHandler, basicConfig

from majsoulrpa import RPA, config
from majsoulrpa.presentation import (
    AuthPresentation,
    HomePresentation,
    LoginPresentation,
)
from majsoulrpa.yostar_login import YostarLoginS3

LOG_LEVEL = INFO
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

            auth_start_time = datetime.datetime.now(datetime.UTC)
            login_s3 = YostarLoginS3(my_config)
            presentation.enter_email_address(login_s3.get_email_address())
            auth_code = login_s3.get_auth_code(start_time=auth_start_time)

            presentation.enter_auth_code(auth_code, timeout=60.0)
            if presentation.new_presentation is None:
                msg = "Could not transit to `home`."
                raise RuntimeError
            presentation = presentation.new_presentation

        if not isinstance(presentation, HomePresentation):
            msg = "Could not transit to `home`."
            raise RuntimeError(msg)

        time.sleep(5.0)
