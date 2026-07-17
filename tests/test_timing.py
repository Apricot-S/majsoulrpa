from random import Random

import pytest

from majsoulrpa.timing import get_random_delay


def test_get_random_delay_returns_positive_delay() -> None:
    delay = get_random_delay(0.1, rng=Random(0))

    assert delay > 0


def test_get_random_delay_accepts_zero_sigma() -> None:
    assert get_random_delay(0.1, sigma=0, rng=Random(0)) == 0.1


def test_get_random_delay_rejects_invalid_parameters() -> None:
    with pytest.raises(ValueError, match="base_delay"):
        get_random_delay(0, rng=Random(0))

    with pytest.raises(ValueError, match="sigma"):
        get_random_delay(0.1, sigma=-0.1, rng=Random(0))
