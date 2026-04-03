from typing import Dict, Type
from src.contracts.task_source import TaskSource


class SourceRepository:
    """
    Хранилище доступных источников
    """

    def __init__(self):
        self._sources: Dict[str, Type[TaskSource]] = {}

    def register(self, name: str, source_cls: Type[TaskSource]):
        self._sources[name] = source_cls

    def get(self, name: str) -> Type[TaskSource]:
        return self._sources[name]