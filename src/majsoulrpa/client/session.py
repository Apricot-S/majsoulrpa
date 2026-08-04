from majsoulrpa.sniffer.events import (
    DecodedRequestResponse,
    DecodedSnifferMessage,
)

OAUTH2_LOGIN_API_NAME = ".lq.Lobby.oauth2Login"
CREATE_ROOM_API_NAME = ".lq.Lobby.createRoom"


class AccountIDMismatchError(RuntimeError):
    """Raised when one client session observes different account IDs."""


class AccountIDDecodeError(RuntimeError):
    """Raised when a known account ID field has an invalid type."""


class SessionState:
    def __init__(self) -> None:
        self._account_id: int | None = None

    @property
    def account_id(self) -> int | None:
        return self._account_id

    def observe(self, message: DecodedSnifferMessage) -> None:
        account_id = _extract_account_id(message)
        if account_id is None:
            return

        if self._account_id is None:
            self._account_id = account_id
            return
        if self._account_id != account_id:
            msg = "Inconsistent account IDs were observed in one session."
            raise AccountIDMismatchError(msg)


def _extract_account_id(message: DecodedSnifferMessage) -> int | None:
    if not isinstance(message, DecodedRequestResponse):
        return None

    if message.raw.name == OAUTH2_LOGIN_API_NAME:
        if "account_id" not in message.response:
            return None
        value = message.response["account_id"]
    elif message.raw.name == CREATE_ROOM_API_NAME:
        if "room" not in message.response:
            return None
        room = message.response["room"]
        if not isinstance(room, dict):
            msg = "Room in a decoded createRoom message must be an object."
            raise AccountIDDecodeError(msg)
        if "owner_id" not in room:
            return None
        value = room["owner_id"]
    else:
        return None

    if isinstance(value, bool) or not isinstance(value, int):
        msg = "Account ID in a decoded message must be an integer."
        raise AccountIDDecodeError(msg)
    if value <= 0:
        return None
    return value
