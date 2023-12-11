# ruff: noqa: N802
import argparse
import asyncio

import grpc  # type:ignore[import-untyped]

from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2 import (
    Message,
    NoneResponse,
    Timeout,
)
from majsoulrpa._impl.protobuf_grpc.grpcserver_pb2_grpc import (
    GRPCServerServicer,
    add_GRPCServerServicer_to_server,
)


class GRPCServer(GRPCServerServicer):

    def __init__(self) -> None:
        super().__init__()
        self._message_queue: asyncio.Queue[bytes] = asyncio.Queue()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def _push_impl(self, content: bytes) -> None:
        self._message_queue.put_nowait(content)

    def PushMessage(self, request: Message, context) -> NoneResponse:  # noqa: ARG002, ANN001
        self._loop.run_in_executor(None, self._push_impl, request.content)
        return NoneResponse()

    async def _pop_impl(self, timeout: float) -> bytes:
        try:
            coro = asyncio.wait_for(self._message_queue.get(), timeout)
            result = await self._loop.create_task(coro)
        except TimeoutError:
            return b""
        else:
            return result

    def PopMessage(self, request: Timeout, context) -> Message:  # noqa: ARG002, ANN001
        result = self._loop.run_until_complete(self._pop_impl(request.seconds))
        return Message(content=result)


async def serve(port: int = 37247) -> None:
    server = grpc.aio.server()
    add_GRPCServerServicer_to_server(GRPCServer(), server)
    server.add_insecure_port(f"[::]:{port}")
    await server.start()
    await server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=37247)
    port: int = parser.parse_args().port
    if (port < 1024) or (port > 49151):  # noqa: PLR2004
        msg = "Port number must be in the range 1024 to 49151."
        raise ValueError(msg)
    asyncio.run(serve(port))
