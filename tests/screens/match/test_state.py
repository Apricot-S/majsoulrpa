from dataclasses import FrozenInstanceError

import pytest

from majsoulrpa.screens.match import (
    Angang,
    Babei,
    Chi,
    Daminggang,
    Dapai,
    Fulu,
    Jiagang,
    Peng,
    validate_seat,
    validate_tile,
)


def _replace_field(value: object, name: str, replacement: object) -> None:
    setattr(value, name, replacement)


def test_fulu_is_a_union_of_concrete_state_types() -> None:
    assert Fulu.__value__ == Chi | Peng | Daminggang | Angang | Jiagang


def test_babei_preserves_moqie_without_joining_fulu_union() -> None:
    babei = Babei(moqie=True)

    assert babei.moqie
    assert Babei not in Fulu.__value__.__args__


def test_concrete_fulu_preserves_variant_specific_fields() -> None:
    from_seat = validate_seat(3)
    tile = validate_tile("1m")
    chi_consumed = (validate_tile("2m"), validate_tile("3m"))
    peng_consumed = (validate_tile("1m"), validate_tile("1m"))
    gang_consumed = (*peng_consumed, validate_tile("1m"))
    angang_consumed = (
        validate_tile("0m"),
        validate_tile("5m"),
        validate_tile("5m"),
        validate_tile("5m"),
    )

    assert (
        Chi(
            from_seat=from_seat,
            tile=tile,
            consumed=chi_consumed,
        ).consumed
        == chi_consumed
    )
    assert (
        Peng(
            from_seat=from_seat,
            tile=tile,
            consumed=peng_consumed,
        ).tile
        == tile
    )
    assert (
        Daminggang(
            from_seat=from_seat,
            tile=tile,
            consumed=gang_consumed,
        ).from_seat
        == from_seat
    )
    assert Angang(consumed=angang_consumed).consumed == angang_consumed
    jiagang = Jiagang(
        from_seat=from_seat,
        tile=validate_tile("5m"),
        consumed=(validate_tile("0m"), validate_tile("5m")),
        added=validate_tile("5m"),
    )
    assert jiagang.consumed == ("0m", "5m")
    assert jiagang.added == "5m"


def test_dapai_babei_and_concrete_fulu_are_frozen() -> None:
    dapai = Dapai(
        tile=validate_tile("1m"),
        moqie=False,
        liqi=False,
        wliqi=False,
    )
    chi = Chi(
        from_seat=validate_seat(3),
        tile=validate_tile("1m"),
        consumed=(validate_tile("2m"), validate_tile("3m")),
    )
    babei = Babei(moqie=False)

    with pytest.raises(FrozenInstanceError):
        _replace_field(dapai, "moqie", replacement=True)
    with pytest.raises(FrozenInstanceError):
        _replace_field(babei, "moqie", replacement=True)
    with pytest.raises(FrozenInstanceError):
        _replace_field(
            chi,
            "tile",
            replacement=validate_tile("4m"),
        )
