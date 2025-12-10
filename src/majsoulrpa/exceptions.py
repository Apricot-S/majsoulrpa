import datetime
from pathlib import Path


class UserInputError(ValueError):
    """Error raised when the user provides invalid input."""


class UnknownAPIError(Exception):
    def __init__(self, name: str, data: bytes) -> None:
        now = datetime.datetime.now(datetime.UTC)
        self._timestamp = now.strftime("%Y-%m-%d-%H-%M-%S")
        super().__init__(f"unknown API '{name}' detected")
        self._name = name
        self._data = data

    @property
    def data(self) -> bytes:
        return self._data

    def save_data(self, directory: Path) -> None:
        file_name = f"{self._timestamp}-{self._name}.bin"
        file_path = directory / Path(file_name)
        with file_path.open("wb") as fp:
            fp.write(self._data)
