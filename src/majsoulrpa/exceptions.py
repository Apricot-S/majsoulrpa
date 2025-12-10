from majsoulrpa.sniffer.exceptions import UnknownAPIError


class UserInputError(ValueError):
    """Error raised when the user provides invalid input."""


__all__ = [
    "UnknownAPIError",
    "UserInputError",
]
