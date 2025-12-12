import asyncio
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue
from typing import Any

from majsoulrpa import RPAClient
from majsoulrpa.presentation.home import HomePresentation
from majsoulrpa.presentation.login import LoginPresentation


def setup_async_logging() -> QueueListener:
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d - %(message)s",  # noqa: E501
    )
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log_queue: Queue[Any] = Queue()
    queue_handler = QueueHandler(log_queue)
    listener = QueueListener(log_queue, stream_handler)

    root = logging.getLogger()
    root.addHandler(queue_handler)
    root.setLevel(logging.DEBUG)

    return listener


rpa = RPAClient()


@rpa.on(LoginPresentation)
async def on_login(p: LoginPresentation, data: Any) -> Any:
    email_address = input("Enter your email address: ")
    async with asyncio.timeout(30):
        await p.enter_email_address(email_address)

    verification_code = input("Enter the verification code: ")
    async with asyncio.timeout(30):
        await p.enter_verification_code(verification_code)

    return [*data, 1]


@rpa.on(HomePresentation)
async def on_home(p: HomePresentation, data: Any) -> Any:
    await asyncio.sleep(5)

    async with asyncio.timeout(5):
        await p.end_rpa(close_browser=True)

    return [*data, 2]


async def main() -> None:
    listener = setup_async_logging()
    listener.start()

    config = RPAClient.Config()
    data_in = [0]
    data_out = await rpa.run(config, data_in, detection_timeout=30)
    print(f"{data_out=}")

    listener.stop()


if __name__ == "__main__":
    asyncio.run(main())
