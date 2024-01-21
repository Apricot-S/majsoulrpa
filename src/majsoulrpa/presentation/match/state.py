# ruff: noqa: PLR2004, S101
import re
from collections.abc import Iterable, Mapping
from typing import Any

from majsoulrpa.common import Player
from majsoulrpa.presentation.presentation_base import InconsistentMessageError


class MatchPlayer(Player):
    def __init__(
        self,
        account_id: int,
        name: str,
        level4: str,
        level3: str,
        character: str,
    ) -> None:
        super().__init__(account_id, name)
        self._level4 = level4
        self._level3 = level3
        self._character = character

    @property
    def level4(self) -> str:
        return self._level4

    @property
    def level3(self) -> str:
        return self._level3

    @property
    def character(self) -> str:
        return self._character


class MatchState:
    def __init__(self) -> None:
        self._uuid: str | None = None
        self._seat: int | None = None
        self._players: list[MatchPlayer] = []

    def _set_uuid(self, uuid: str) -> None:
        if self._uuid is None:
            self._uuid = uuid
        elif uuid != self._uuid:
            msg = (
                "An inconsistent UUIDs.\n"
                f"Old one: {self._uuid}\n"
                f"New one: {uuid}"
            )
            raise ValueError(msg)

    def _set_seat(self, seat: int) -> None:
        if self._seat is not None:
            msg = "`seat` is already set."
            raise RuntimeError(msg)
        self._seat = seat

    def _set_players(self, players: Iterable[MatchPlayer]) -> None:
        if self._players:
            msg = "`players` is already set."
            raise RuntimeError(msg)
        self._players = list(players)

    @property
    def uuid(self) -> str:
        if self._uuid is None:
            msg = "`uuid` has not been initialized yet."
            raise ValueError(msg)
        return self._uuid

    @property
    def seat(self) -> int:
        if self._seat is None:
            msg = "`seat` has not been initialized yet."
            raise ValueError(msg)
        return self._seat

    @property
    def players(self) -> list[MatchPlayer]:
        if not self._players:
            msg = "`players` have not been initialized yet."
            raise ValueError(msg)
        return self._players


class RoundState:
    def __init__(
        self,
        match_state: MatchState,
        data: Mapping[str, Any],
    ) -> None:
        self._match_state = match_state
        self._chang = data["chang"]
        self._ju = data["ju"]
        self._ben = data["ben"]
        self._liqibang = data["liqibang"]
        self._dora_indicators = data["doras"]
        self._left_tile_count = data["left_tile_count"]
        self._scores = data["scores"]
        self._shoupai = data["tiles"][:13]
        if len(data["tiles"]) == 14:
            self._zimopai = data["tiles"][13]
        else:
            self._zimopai = None
        self._num_player = len(self._scores)
        self._he: list[list] = [[]] * self._num_player
        self._fulu: list[list] = [[]] * self._num_player
        self._num_babei: list[int] = [0] * self._num_player
        self._liqi = [False] * self._num_player
        self._wliqi = [False] * self._num_player
        self._first_draw = [True] * self._num_player
        self._yifa = [False] * self._num_player
        self._lingshang_zimo = [False] * self._num_player
        self._prev_dapai_seat: int | None = None
        self._prev_dapai: str | None = None

    _pattern1 = re.compile("^([1-9])([mpsz])$")
    _pattern2 = re.compile("^0([mps])$")
    _pattern3 = re.compile("^([mps])5!$")
    _pattern4 = re.compile("^([mpsz])([1-9])@$")

    def _hand_in(self) -> None:
        # Incorporate the drawn tile into the hand
        # and sort the hand
        assert self._zimopai is not None
        self._shoupai.append(self._zimopai)
        self._zimopai = None

        # sort the hand
        shoupai = [
            RoundState._pattern1.sub(r"\2\1@", t) for t in self._shoupai
        ]
        shoupai = [RoundState._pattern2.sub(r"\g<1>5!", t) for t in shoupai]
        shoupai.sort()
        shoupai = [RoundState._pattern3.sub(r"0\1", t) for t in shoupai]
        self._shoupai = [RoundState._pattern4.sub(r"\2\1", t) for t in shoupai]

    def _on_zimo(self, data: Mapping[str, Any]) -> None:
        if data["seat"] == self._match_state.seat:
            assert self._zimopai is None
            self._zimopai = data["tile"]
        else:
            if data["tile"] != "":
                msg = (
                    f"data['seat'] = {data['seat']}, "
                    f"data['tile'] = {data['tile']}"
                )
                raise ValueError(msg)
            if "operation" in data:
                raise ValueError

        if len(data["doras"]) > 0:
            # Display new dora.
            self._dora_indicators = data["doras"]
        self._left_tile_count = data["left_tile_count"]

        if "liqi" in data:
            liqi = data["liqi"]
            self._scores[liqi["seat"]] = liqi["score"]
            self._liqibang += 1

        self._prev_dapai_seat = None
        self._prev_dapai = None

    def _on_dapai(self, data: Mapping[str, Any]) -> None:
        assert self._prev_dapai_seat is None
        assert self._prev_dapai is None

        seat = data["seat"]

        if seat == self._match_state.seat:
            if data["moqie"]:
                assert self._zimopai is not None
                assert self._zimopai == data["tile"]
                self._zimopai = None
            else:
                # discarding from the hand
                index = None
                for i, tile in enumerate(self._shoupai):
                    if tile == data["tile"]:
                        index = i
                        break
                if index is None:
                    # If you are the parent
                    # and the first discaring a tile in the hand.
                    assert seat == self._ju
                    assert self._first_draw[seat]
                    assert self._zimopai is not None
                    assert self._zimopai == data["tile"]
                    self._zimopai = None
                else:
                    self._shoupai.pop(index)
                    if self._zimopai is not None:
                        # Incorporate the drawn tile into the hand.
                        self._hand_in()
            assert "operation" not in data

        if len(data["doras"]) > 0:
            # Display new dora.
            self._dora_indicators = data["doras"]

        self._he[seat].append((data["tile"], data["moqie"]))

        if data["is_liqi"]:
            self._liqi[seat] = True
            self._yifa[seat] = True
        elif data["is_wliqi"]:
            self._wliqi[seat] = True
            self._yifa[seat] = True
        else:
            self._yifa[seat] = False
        self._first_draw[seat] = False
        self._lingshang_zimo[seat] = False

        self._prev_dapai_seat = seat
        self._prev_dapai = data["tile"]

    def _on_chipenggang(self, data: Mapping[str, Any]) -> None:
        seat = data["seat"]

        assert self._prev_dapai_seat is not None
        assert seat != self._prev_dapai_seat
        assert self._prev_dapai is not None

        if seat == self._match_state.seat:
            # Remove the melds from the hand.
            for tile in data["tiles"][:-1]:
                for i, t in enumerate(self._shoupai):
                    if t == tile:
                        assert i < len(self._shoupai)
                        self._shoupai.pop(i)
                        break

        assert self._zimopai is None

        type_ = ("チー", "ポン", "大明槓")[data["type"]]
        from_ = data["froms"][-1]
        he_index = len(self._he[from_]) - 1
        self._fulu[seat].append((type_, from_, he_index, data["tiles"]))

        if "liqi" in data:
            liqi = data["liqi"]
            self._scores[liqi["seat"]] = liqi["score"]
            self._liqibang += 1

        self._first_draw = [False] * self._num_player
        self._yifa = [False] * self._num_player
        if type_ == "大明槓":
            self._lingshang_zimo[seat] = True

        self._prev_dapai_seat = None
        self._prev_dapai = None

        assert (seat == self._match_state.seat) or ("operation" not in data)

    def _on_angang_jiagang(self, data: Mapping[str, Any]) -> None:  # noqa: C901
        assert self._prev_dapai_seat is None
        assert self._prev_dapai is None

        seat = data["seat"]

        assert (seat == self._match_state.seat) == (self._zimopai is not None)

        if seat == self._match_state.seat:
            # Remove the melds from the hand or drawn tile.
            tiles: tuple[str] | tuple[str, str] | None = None
            if data["tiles"] in ("0m", "5m"):
                tiles = ("0m", "5m")
            elif data["tiles"] in ("0p", "5p"):
                tiles = ("0p", "5p")
            elif data["tiles"] in ("0s", "5s"):
                tiles = ("0s", "5s")
            else:
                assert isinstance(data["tiles"], str)
                tiles = (data["tiles"],)
            count = 0
            i = 0
            while i < len(self._shoupai):
                tile = self._shoupai[i]
                if tile in tiles:
                    self._shoupai.pop(i)
                    count += 1
                    continue
                i += 1
            if data["type"] == 2:
                # In case of Jiagang
                if count != 1:
                    if count != 0:
                        msg = "An inconsistent message"
                        raise InconsistentMessageError(msg)
                    if self._zimopai is None:
                        msg = "An inconsistent message"
                        raise InconsistentMessageError(msg)
                    if self._zimopai not in tiles:
                        msg = "An inconsistent message"
                        raise InconsistentMessageError(msg)
                    self._zimopai = None
                    count += 1
                assert count == 1
            elif data["type"] == 3:
                # In case of Angang
                if count != 4:
                    if count != 3:
                        msg = "An inconsistent message"
                        raise InconsistentMessageError(msg)
                    if self._zimopai is None:
                        msg = "An inconsistent message"
                        raise InconsistentMessageError(msg)
                    if self._zimopai not in tiles:
                        msg = "An inconsistent message"
                        raise InconsistentMessageError(msg)
                    self._zimopai = None
                    count += 1
                assert count == 4

            if self._zimopai is not None:
                # Incorporate the drawn tile into the hand.
                self._hand_in()

        assert data["type"] in (2, 3)
        type_ = (None, None, "加槓", "暗槓")[data["type"]]
        if data["type"] == 2:
            # In the case of Jiagang,
            # replace the existing Peng with Jiagang.
            for i, fulu in enumerate(self._fulu[seat]):
                if fulu[3] == data["tiles"][:-1]:
                    assert i < len(self._fulu[seat])
                    from_ = self._fulu[seat][i][1]
                    he_index = self._fulu[seat][i][2]
                    self._fulu[seat][i] = (
                        type_,
                        from_,
                        he_index,
                        data["tiles"],
                    )
                    break
        else:
            # In case of Angang
            self._fulu[seat].append((type_, None, None, data["tiles"]))

        if len(data["doras"]) > 0:
            # Display new dora.
            self._dora_indicators = data["doras"]

        self._first_draw = [False] * self._num_player
        self._yifa = [False] * self._num_player
        self._lingshang_zimo[seat] = True

        # Since there is a Qianggang,
        # Angang and Jiagang are considered discarded tiles.
        self._prev_dapai_seat = seat
        self._prev_dapai = data["tiles"][-1]

    def _on_babei(self, data: Mapping[str, Any]) -> None:
        assert self._prev_dapai_seat is None
        assert self._prev_dapai is None

        seat = data["seat"]

        assert (seat == self._match_state.seat) == (self._zimopai is not None)

        bei = "4z"

        if seat == self._match_state.seat:
            # Remove the melds from the hand or drawn tile.
            count = 0
            if bei in self._shoupai:
                self._shoupai.remove(bei)
                count += 1

            if count != 1:
                if count != 0:
                    msg = "An inconsistent message"
                    raise InconsistentMessageError(msg)
                if self._zimopai is None:
                    msg = "An inconsistent message"
                    raise InconsistentMessageError(msg)
                if self._zimopai != bei:
                    msg = "An inconsistent message"
                    raise InconsistentMessageError(msg)
                self._zimopai = None
                count += 1
            assert count == 1

            if self._zimopai is not None:
                # Incorporate the drawn tile into the hand.
                self._hand_in()

        self._first_draw = [False] * self._num_player
        self._yifa = [False] * self._num_player
        self._num_babei[seat] += 1
        self._lingshang_zimo[seat] = True

        # Since there is a Qianggang,
        # Babei is considered discarded tiles.
        self._prev_dapai_seat = seat
        self._prev_dapai = bei

    @property
    def chang(self) -> int:
        assert self._chang >= 0
        assert self._chang < 3
        return self._chang

    @property
    def ju(self) -> int:
        assert self._ju >= 0
        assert self._ju < 4
        return self._ju

    @property
    def ben(self) -> int:
        assert self._ben >= 0
        return self._ben

    @property
    def liqibang(self) -> int:
        assert self._liqibang >= 0
        return self._liqibang

    @property
    def dora_indicators(self) -> list[str]:
        assert len(self._dora_indicators) >= 1
        assert len(self._dora_indicators) <= 5
        return self._dora_indicators

    @property
    def left_tile_count(self) -> int:
        assert self._left_tile_count >= 0
        assert self._left_tile_count < 70
        return self._left_tile_count

    @property
    def scores(self) -> list[int]:
        assert len(self._scores) in (4, 3)
        return self._scores

    @property
    def shoupai(self) -> list[str]:
        return self._shoupai

    @property
    def zimopai(self) -> str | None:
        return self._zimopai

    @property
    def he(self) -> list[list[tuple[str, bool]]]:
        assert len(self._he) in (4, 3)
        for he_ in self._he:
            assert len(he_) <= 24
        return self._he

    @property
    def fulu(
        self,
    ) -> list[list[tuple[str, int | None, int | None, list[str]]]]:
        assert len(self._fulu) in (4, 3)
        for fulu_ in self._fulu:
            for type_, from_, he_index, tiles in fulu_:
                assert type_ in ("チー", "ポン", "大明槓", "暗槓", "加槓")
                assert from_ != self._match_state.seat
                assert from_ >= 0
                assert from_ < 4
                assert he_index < len(self._fulu[from_])
                assert type_ not in ("チー", "ポン") or len(tiles) == 3
                assert (
                    type_ not in ("大明槓", "暗槓", "加槓") or len(tiles) == 4
                )
        return self._fulu

    @property
    def num_babei(self) -> list[int]:
        assert len(self._num_babei) == 3
        return self._num_babei

    @property
    def liqi(self) -> list[bool]:
        assert len(self._liqi) in (4, 3)
        assert len(self._liqi) == len(self._wliqi)
        for i in range(len(self._liqi)):
            assert not (self._liqi[i] and self._wliqi[i])
        return self._liqi

    @property
    def wliqi(self) -> list[bool]:
        assert len(self._wliqi) in (4, 3)
        assert len(self._wliqi) == len(self._liqi)
        for i in range(len(self._wliqi)):
            assert not (self._liqi[i] and self._wliqi[i])
        return self._wliqi

    @property
    def first_draw(self) -> list[bool]:
        assert len(self._first_draw) in (4, 3)
        return self._first_draw

    @property
    def yifa(self) -> list[bool]:
        assert len(self._yifa) in (4, 3)
        return self._yifa

    @property
    def lingshang_zimo(self) -> list[bool]:
        assert len(self._lingshang_zimo) in (4, 3)
        return self._lingshang_zimo

    @property
    def prev_dapai_seat(self) -> int | None:
        return self._prev_dapai_seat

    @property
    def prev_dapai(self) -> str | None:
        return self._prev_dapai
