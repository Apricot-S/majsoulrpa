from pathlib import Path
from typing import override

from majsoulrpa._majsoul_internal.protocol import liqi_pb2
from majsoulrpa.sniffer.addon import SniffedMessage, Sniffer


def get_log_id(message: bytes) -> str:
    wrapper = liqi_pb2.Wrapper()
    wrapper.ParseFromString(message[3:])

    if wrapper.name != "":
        msg = f"an unexpected API name: {wrapper.name}"
        raise RuntimeError(msg)

    parser = liqi_pb2.ResGameRecord()
    parser.ParseFromString(wrapper.data)

    return parser.head.uuid


class LogArchiver(Sniffer):
    @override
    def on_sniffed_message(self, sniffed: SniffedMessage) -> None:
        if sniffed.name != ".lq.Lobby.fetchGameRecord":
            return

        response = sniffed.response
        if response is None:
            msg = f"{sniffed.name}: missing response"
            raise RuntimeError(msg)

        log_id = get_log_id(response)
        file_path = Path(f"./{log_id}.bin")

        with file_path.open(mode="wb") as f:
            f.write(response)


addons = [LogArchiver()]
