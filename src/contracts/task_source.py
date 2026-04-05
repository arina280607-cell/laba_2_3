from collections.abc import Iterable
from typing import Protocol, runtime_checkable

from src.contracts.tasks import Task


@runtime_checkable#для проверки наличия атрибутов
class TaskSource(Protocol):
    """
    контракт для всех источников задач
    любой источник должен реализовать метод get_tasks
    """
    name: str
    def get_tasks(self) -> Iterable[Task]: ...
