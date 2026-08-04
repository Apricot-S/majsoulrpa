import asyncio
from collections.abc import Collection, Sequence
from typing import Any


async def cancel_tasks(
    tasks: Collection[asyncio.Future[Any]],
) -> list[BaseException]:
    for task in tasks:
        if not task.done():
            task.cancel()

    errors: list[BaseException] = []
    for task in tasks:
        try:
            await task
        except asyncio.CancelledError:
            pass
        except BaseException as error:  # noqa: BLE001
            errors.append(error)
    return errors


def raise_task_errors(
    errors: Sequence[BaseException],
    *,
    group_message: str,
) -> None:
    if len(errors) == 1:
        raise errors[0]
    if errors:
        raise BaseExceptionGroup(group_message, errors)
