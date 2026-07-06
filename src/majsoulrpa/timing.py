from random import Random

DEFAULT_DELAY_SIGMA = 0.1
_DEFAULT_RANDOM = Random()  # noqa: S311


def get_random_delay(
    base_delay: float,
    *,
    sigma: float = DEFAULT_DELAY_SIGMA,
    rng: Random | None = None,
) -> float:
    if base_delay <= 0:
        msg = "base_delay must be positive."
        raise ValueError(msg)
    if sigma < 0:
        msg = "sigma must be non-negative."
        raise ValueError(msg)
    if sigma == 0:
        return base_delay

    random_source = rng or _DEFAULT_RANDOM
    stddev = base_delay * sigma
    while True:
        delay = random_source.normalvariate(base_delay, stddev)
        if delay > 0:
            return delay
