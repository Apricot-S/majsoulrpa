from random import Random

import pytest

from majsoulrpa.timing import get_random_delay


class SequenceRandom(Random):
    def __init__(self, values: list[float]) -> None:
        self._values = iter(values)

    def normalvariate(self, mu: float = 0.0, sigma: float = 1.0) -> float:
        _ = mu, sigma
        return next(self._values)


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


@pytest.mark.parametrize(
    ("base_delay", "sigma"),
    [
        (float("nan"), 0.25),
        (float("inf"), 0.25),
        (0.1, float("nan")),
        (0.1, float("inf")),
    ],
)
def test_get_random_delay_rejects_non_finite_parameters(
    base_delay: float,
    sigma: float,
) -> None:
    with pytest.raises(ValueError, match="finite"):
        get_random_delay(
            base_delay,
            sigma=sigma,
            rng=SequenceRandom([0.1]),
        )


def test_get_random_delay_resamples_until_delay_is_positive() -> None:
    delay = get_random_delay(
        0.1,
        rng=SequenceRandom([-0.1, 0.0, 0.2]),
    )

    assert delay == 0.2
