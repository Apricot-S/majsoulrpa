class Player:
    """Player."""

    def __init__(self, account_id: int, name: str) -> None:
        """Initializes the instance.

        Args:
            account_id: Player's account ID.
            name: Player's name.
        """
        self._account_id = account_id
        self._name = name

    @property
    def account_id(self) -> int:
        """Player's account ID."""
        return self._account_id

    @property
    def name(self) -> str:
        """Player's name."""
        return self._name
