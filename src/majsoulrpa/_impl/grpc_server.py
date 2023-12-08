# ruff: noqa: N802, T201
import argparse
import asyncio
from concurrent import futures

import grpc

from majsoulrpa._impl.grpcserver.grpcserver_pb2 import (
    Message,
    NoneResponse,
    Timeout,
)
from majsoulrpa._impl.grpcserver.grpcserver_pb2_grpc import (
    GRPCServerServicer,
    add_GRPCServerServicer_to_server,
)


class GRPCServer(GRPCServerServicer):

    def __init__(self) -> None:
        super().__init__()
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)

    def PushMessage(
        self, request: Message, context: grpc.ServicerContext,  # noqa: ARG002
    ) -> NoneResponse:
        self._loop.run_until_complete(self._message_queue.put(request.content))
        size = self._message_queue.qsize()
        print(f"Pushed. Size of message_queue: {size}")
        return NoneResponse()

    def PopMessage(
        self, request: Timeout, context: grpc.ServicerContext,  # noqa: ARG002
    ) -> Message:
        try:
            content = self._loop.run_until_complete(
                asyncio.wait_for(self._message_queue.get(), request.seconds),
            )
        except TimeoutError:
            size = self._message_queue.qsize()
            print(f"Empty. Size of message_queue: {size}")
            return Message(content=None)
        else:
            size = self._message_queue.qsize()
            print(f"Popped. Size of message_queue: {size}")
            return Message(content=content)


def serve(port: int = 37247) -> None:
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    add_GRPCServerServicer_to_server(GRPCServer(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=37247)
    port: int = parser.parse_args().port
    if (port < 1024) or (port > 49151):  # noqa: PLR2004
        msg = "Port number must be in the range 1024 to 49151."
        raise ValueError(msg)
    print(f"Listening on port {port}...")
    serve(port)
