# ruff: noqa: PLR2004, S101
from collections.abc import Iterable, Iterator, Mapping
from typing import Any


class DapaiOperation:

    def __init__(self, forbidden_tiles: Iterable[str]) -> None:
        self._forbidden_tiles = list(forbidden_tiles)

    @property
    def type_(self) -> str:
        return "打牌"

    @property
    def forbidden_tiles(self) -> list[str]:
        return self._forbidden_tiles


class ChiOperation:

    def __init__(self, combinations: Iterable[str]) -> None:
        self._combinations: list[tuple[str, str]] = []
        for combination in combinations:
            tiles = combination.split("|")
            assert len(tiles) == 2
            self._combinations.append(tuple(tiles)) # type: ignore[arg-type]

    @property
    def type_(self) -> str:
        return "チー"

    @property
    def combinations(self) -> list[tuple[str, str]]:
        return self._combinations


class PengOperation:

    def __init__(self, combinations: Iterable[str]) -> None:
        self._combinations: list[tuple[str, str]] = []
        for combination in combinations:
            tiles = combination.split("|")
            assert len(tiles) == 2
            self._combinations.append(tuple(tiles)) # type: ignore[arg-type]

    @property
    def type_(self) -> str:
        return "ポン"

    @property
    def combinations(self) -> list[tuple[str, str]]:
        return self._combinations


class AngangOperation:
    def __init__(self, combinations: Iterable[str]) -> None:
        self._combinations: list[tuple[str, str, str, str]] = []
        for combination in combinations:
            tiles = combination.split("|")
            assert len(tiles) == 4
            self._combinations.append(tuple(tiles)) # type: ignore[arg-type]

    @property
    def type_(self) -> str:
        return "暗槓"

    @property
    def combinations(self) -> list[tuple[str, str, str, str]]:
        return self._combinations


class DaminggangOperation:

    def __init__(self, combinations: Iterable[str]) -> None:
        self._combinations: list[tuple[str, str, str]] = []
        for combination in combinations:
            tiles = combination.split("|")
            assert len(tiles) == 3
            self._combinations.append(tuple(tiles)) # type: ignore[arg-type]

    @property
    def type_(self) -> str:
        return "大明槓"

    @property
    def combinations(self) -> list[tuple[str, str, str]]:
        return self._combinations


class JiagangOperation:

    def __init__(self, combinations: Iterable[str]) -> None:
        self._combinations: list[tuple[str, str, str, str]] = []
        for combination in combinations:
            tiles = combination.split("|")
            assert len(tiles) == 4
            self._combinations.append(tuple(tiles)) # type: ignore[arg-type]

    @property
    def type_(self) -> str:
        return "加槓"

    @property
    def combinations(self) -> list[tuple[str, str, str, str]]:
        return self._combinations


class LiqiOperation:

    def __init__(self, combinations: Iterable[str]) -> None:
        self._candidate_dapai_list = list(combinations)

    @property
    def type_(self) -> str:
        return "立直"

    @property
    def candidate_dapai_list(self) -> list[str]:
        return self._candidate_dapai_list


class ZimohuOperation:

    def __init__(self) -> None:
        pass

    @property
    def type_(self) -> str:
        return "自摸和"


class RongOperation:
    def __init__(self) -> None:
        pass

    @property
    def type_(self) -> str:
        return "ロン"


class JiuzhongjiupaiOperation:
    def __init__(self) -> None:
        pass

    @property
    def type_(self) -> str:
        return "九種九牌"


class OperationList:
    def __init__(self, operation_list: Mapping[str, Any]) -> None:
        self._basic_time = operation_list["time_fixed"]
        self._extra_time = operation_list["time_add"]
        self._operations = []
        op: Any = None
        for operation in operation_list["operation_list"]:
            match operation["type"]:
                case 1:
                    op = DapaiOperation(operation["combination"])
                    self._operations.append(op)
                case 2:
                    op = ChiOperation(operation["combination"])
                    self._operations.append(op)
                case 3:
                    op = PengOperation(operation["combination"])
                    self._operations.append(op)
                case 4:
                    op = AngangOperation(operation["combination"])
                    self._operations.append(op)
                case 5:
                    op = DaminggangOperation(operation["combination"])
                    self._operations.append(op)
                case 6:
                    op = JiagangOperation(operation["combination"])
                    self._operations.append(op)
                case 7:
                    op = LiqiOperation(operation["combination"])
                    self._operations.append(op)
                case 8:
                    op = ZimohuOperation()
                    self._operations.append(op)
                case 9:
                    op = RongOperation()
                    self._operations.append(op)
                case 10:
                    op = JiuzhongjiupaiOperation()
                    self._operations.append(op)
                case _:
                    msg = f'type == {operation["type"]}'
                    raise ValueError(msg)

    @property
    def basic_time(self) -> int:
        return self._basic_time // 1000

    @property
    def extra_time(self) -> int:
        return self._extra_time // 1000

    def __iter__(self) -> Iterator[Any]:
        return iter(self._operations)
