class Player:
    def __init__(self, account_id: int, name: str) -> None:
        self._account_id = account_id
        self._name = name

    @property
    def account_id(self) -> int:
        return self._account_id

    @property
    def name(self) -> str:
        return self._name
