from collections.abc import Iterator, Iterable
from typing import Generator
from src.contracts.tasks import Task

class TaskQueue:
    """
    Очередь задач с поддержкой итерации и ленивой фильтрации.
    """

    def __init__(self, tasks: Iterable[Task] | None = None):
        self._tasks = list(tasks) if tasks else []

    def add(self, task: Task) -> None:
        self._tasks.append(task)

    def __len__(self) -> int:
        return len(self._tasks)

    def __iter__(self) -> Iterator[Task]:
        return iter(self._tasks)

    def __repr__(self) -> str:
        return f"TaskQueue({len(self._tasks)} tasks)"

    # Ленивые генераторы

    def filter_by_status(self, status: str) -> Generator[Task, None, None]:
        for task in self._tasks:
            if task.status == status:
                yield task

    def filter_by_priority(self, min_priority: int) -> Generator[Task, None, None]:
        for task in self._tasks:
            if task.priority >= min_priority:
                yield task

    def ready_tasks(self) -> Generator[Task, None, None]:
        for task in self._tasks:
            if task.is_ready:
                yield task