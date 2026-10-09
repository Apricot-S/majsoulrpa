from dataclasses import replace

import pytest

from majsoulrpa.screens._decode_errors import ScreenDecodeError
from majsoulrpa.screens.match._metadata import (
    decode_match_metadata,
)
from majsoulrpa.screens.room._decode import (
    decode_room_state,
)
from tests.screens.match._support import SELF_ACCOUNT_ID, _auth_game


def test_room_field_failure_uses_screen_decode_error() -> None:
    with pytest.raises(ScreenDecodeError, match=r"room_id"):
        decode_room_state({}, version=1, self_account_id=1)


def test_metadata_field_failure_uses_screen_decode_error() -> None:
    message = replace(_auth_game(), request={"account_id": True})
    with pytest.raises(ScreenDecodeError, match="account_id"):
        decode_match_metadata(message, SELF_ACCOUNT_ID)
