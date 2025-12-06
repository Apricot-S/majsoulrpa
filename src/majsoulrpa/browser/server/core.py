from collections.abc import Awaitable, Callable

import zmq
import zmq.asyncio

from majsoulrpa.browser import schemas
from majsoulrpa.browser.server.config import Config
from majsoulrpa.netutils import make_endpoint

type RequestHandler = Callable[[schemas.Request], Awaitable[schemas.Response]]
type ServerRunner = Callable[[Config, RequestHandler], Awaitable[None]]


async def _server_loop(
    socket: zmq.asyncio.Socket,
    request_handler: RequestHandler,
) -> None:
    while True:
        raw_req = await socket.recv_string()
        req = schemas.REQUEST_ADAPTER.validate_json(raw_req)
        res = await request_handler(req)
        await socket.send_string(res.model_dump_json())
        if isinstance(req, schemas.QuitRequest):
            break


async def run_server(
    config: Config,
    request_handler: RequestHandler,
) -> None:
    with zmq.asyncio.Context() as ctx, ctx.socket(zmq.REP) as socket:
        if config.client_address.version == 6:  # noqa: PLR2004
            socket.setsockopt(zmq.IPV6, 1)

        endpoint = make_endpoint(config.client_address, config.remote_port)

        with socket.bind(f"tcp://{endpoint}"):
            await _server_loop(socket, request_handler)
