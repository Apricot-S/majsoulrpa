from pydantic import BaseModel, ConfigDict, Field

from majsoulrpa.constants import DEFAULT_BROWSER_ADDRESS


def _to_kebab(snake: str) -> str:
    return snake.replace("_", "-")


class ConfigInput(BaseModel):
    model_config = ConfigDict(alias_generator=_to_kebab)

    browser_address: str = Field(DEFAULT_BROWSER_ADDRESS)
