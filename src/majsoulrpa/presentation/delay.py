import random


def get_random_delay(base_delay: float, sigma: float = 0.1) -> float:
    """Returns randomized delay using normal distribution.

    This function generates a delay value centered around the given
    `base_delay` with variability determined by `sigma`. The delay
    is sampled from a normal distribution with mean = `base_delay` and
    standard deviation = `base_delay * sigma`. Negative values are
    rejected to ensure the returned delay is always positive.


    Args:
        base_delay: Base delay.
        sigma: Ratio of standard deviation (e.g., 0.1 -> ±10%).
            Defaults to 0.1.

    Returns:
        A positive randomized delay value sampled from the specified
            normal distribution.
    """
    stddev = base_delay * sigma
    while True:
        delay = random.normalvariate(base_delay, stddev)
        if delay > 0.0:
            return delay
