from majsoulrpa.presentation.match.state import MatchState, RoundState


def test_round_state() -> None:
    match_state = MatchState()
    match_state._seat = 0
    round_state = RoundState(
        match_state,
        data={
            "chang": 0,
            "ju": 0,
            "ben": 0,
            "liqibang": 0,
            "doras": ["2z"],
            "left_tile_count": 70,
            "scores": [25000, 25000, 25000, 25000],
            "tiles": [
                "5s",
                "2m",
                "6m",
                "6z",
                "6z",
                "8m",
                "6z",
                "5s",
                "5z",
                "8p",
                "6p",
                "6s",
                "1s",
                "3p",
            ],
        },
    )

    assert round_state.zimopai == "6z"
    assert round_state.shoupai[0] == "2m"

    round_state._shoupai = [
        "2m",
        "7m",
        "8m",
        "9m",
        "3p",
        "4p",
        "5p",
        "4s",
        "0s",
        "5s",
        "6s",
        "9s",
        "9s",
    ]
    round_state._zimopai = "1m"
    round_state._on_dapai(
        {
            "seat": 0,
            "moqie": False,
            "tile": "5s",
            "doras": [],
            "is_liqi": False,
            "is_wliqi": False,
        },
    )
    assert round_state.zimopai is None
    assert round_state.shoupai[0] == "1m"
    assert "0s" in round_state.shoupai
    assert "5s" not in round_state.shoupai
