import asyncio
from types import SimpleNamespace

import pytest
from pydantic import JsonValue

from majsoulrpa.screens._json_fields import get_dict, get_dict_list
from majsoulrpa.screens.errors import (
    MessageDecodeError,
    ScreenInconsistentMessageError,
)
from majsoulrpa.screens.match import MatchOrigin, MatchRank, MatchScreen
from majsoulrpa.screens.match._metadata import decode_match_metadata
from tests.screens._support import (
    BrowserControllerSpy,
    ScreenContext,
    _message_queue,
)
from tests.screens.match._support import SELF_ACCOUNT_ID, _auth_game


@pytest.mark.parametrize(
    "implicit_robots", [False, True], ids=["robots", "vs-ai"]
)
def test_session_account_must_be_a_human(*, implicit_robots: bool) -> None:
    message = _auth_game(cpu_count=3)
    humans = get_dict_list(message.response, "players")
    humans[0]["account_id"] = 1
    if implicit_robots:
        message.response["robots"] = []
        message.response["ready_id_list"] = [SELF_ACCOUNT_ID, 2, 3]
    else:
        robots = get_dict_list(message.response, "robots")
        robots[0]["account_id"] = SELF_ACCOUNT_ID

    with pytest.raises(MessageDecodeError, match=r"current account.*human"):
        decode_match_metadata(message, SELF_ACCOUNT_ID)


def test_human_name_must_not_be_empty_even_with_cpu_ranks() -> None:
    message = _auth_game()
    human = get_dict_list(message.response, "players")[0]
    human["nickname"] = ""
    human["level3"] = {"id": 20101, "score": 0}

    with pytest.raises(MessageDecodeError, match="human nickname"):
        decode_match_metadata(message, SELF_ACCOUNT_ID)


@pytest.mark.parametrize("player_count", [3, 4])
@pytest.mark.parametrize(
    "tournament", [False, True], ids=["friendly", "tournament"]
)
def test_metadata_preserves_seats_ranks_and_origin(
    player_count: int, *, tournament: bool
) -> None:
    message = _auth_game(
        player_count=player_count,
        room_id=0 if tournament else 12345,
        contest_uid=54321 if tournament else 0,
    )

    metadata = decode_match_metadata(message, SELF_ACCOUNT_ID)

    assert metadata.self_seat == 0
    assert metadata.origin is (
        MatchOrigin.TOURNAMENT if tournament else MatchOrigin.FRIENDLY
    )
    assert metadata.origin_id == (54321 if tournament else 12345)
    assert len(metadata.players) == player_count
    for seat, player in enumerate(metadata.players):
        assert player.seat == seat
        assert player.account_id == SELF_ACCOUNT_ID + seat
        assert player.name == f"player-{seat}"
        assert player.level4 == MatchRank(id=10101 + seat, score=seat)
        assert player.level3 == MatchRank(id=20101 + seat, score=seat + 10)
        assert not player.is_cpu


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("seat_list", [SELF_ACCOUNT_ID, 100002]),
        ("seat_list", [SELF_ACCOUNT_ID, 100002, 100002, 100004]),
        ("seat_list", [SELF_ACCOUNT_ID, 0, 100003, 100004]),
        ("seat_list", [100005, 100002, 100003, 100004]),
        ("players", []),
    ],
    ids=[
        "player-count",
        "duplicate-seat",
        "nonpositive-seat",
        "self-absent",
        "humans-absent",
    ],
)
def test_metadata_rejects_invalid_participant_mapping(
    field: str, value: JsonValue
) -> None:
    message = _auth_game()
    message.response[field] = value

    with pytest.raises(MessageDecodeError):
        decode_match_metadata(message, SELF_ACCOUNT_ID)


@pytest.mark.parametrize("field", ["players", "robots"])
@pytest.mark.parametrize("invalid_id", [0, SELF_ACCOUNT_ID, 999999])
def test_metadata_rejects_nonpositive_duplicate_or_extra_participant(
    field: str, invalid_id: int
) -> None:
    message = _auth_game(cpu_count=1)
    participant = get_dict_list(message.response, field)[0]
    participant["account_id"] = invalid_id
    if field == "players" and invalid_id == SELF_ACCOUNT_ID:
        get_dict_list(message.response, field).append(participant.copy())

    with pytest.raises(MessageDecodeError):
        decode_match_metadata(message, SELF_ACCOUNT_ID)


@pytest.mark.parametrize("rank_name", ["level", "level3"])
@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("id", 0),
        ("score", -1),
        ("score", True),
        ("id", "synthetic-private-value"),
    ],
    ids=[
        "nonpositive-id",
        "negative-score",
        "boolean-score",
        "invalid-id-type",
    ],
)
def test_metadata_rejects_invalid_rank_without_displaying_input(
    rank_name: str, field: str, value: JsonValue
) -> None:
    message = _auth_game()
    human = get_dict_list(message.response, "players")[0]
    get_dict(human, rank_name)[field] = value

    with pytest.raises(MessageDecodeError) as exc_info:
        decode_match_metadata(message, SELF_ACCOUNT_ID)

    assert "synthetic-private-value" not in str(exc_info.value)
    assert "synthetic-secret-token" not in repr(exc_info.value)


def test_screen_preserves_metadata_decode_cause_and_screenshot() -> None:
    message = _auth_game()
    get_dict_list(message.response, "players")[0]["nickname"] = ""
    browser = BrowserControllerSpy(b"synthetic-inconsistent-screenshot")
    screen = MatchScreen(
        ScreenContext(
            browser=browser,
            sniffer_messages=_message_queue(message),
            account_state=SimpleNamespace(account_id=SELF_ACCOUNT_ID),
        )
    )

    with pytest.raises(ScreenInconsistentMessageError) as exc_info:
        asyncio.run(screen.before_callback())

    assert exc_info.value.screenshot == b"synthetic-inconsistent-screenshot"
    assert isinstance(exc_info.value.__cause__, MessageDecodeError)
