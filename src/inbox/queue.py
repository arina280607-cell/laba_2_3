from collections.abc import Iterator, Iterable
from typing import Generator
from src.contracts.tasks import Task

class TaskQueue:
    """
    Очередь задач с поддержкой итерации и ленивой фильтрации.
    """

    def __init__(self, tasks: Iterable[Task] | None = None): #принимает итерируемые данные и инициализирует объект
        self._tasks = list(tasks) if tasks else []

    def add(self, task: Task) -> None:#добавление задачи
        self._tasks.append(task)

    def __len__(self) -> int:#длина очереди
        return len(self._tasks)

    def __iter__(self) -> Iterator[Task]:#итерация
        return iter(self._tasks)

    def __repr__(self) -> str:#приятное представление объекта
        return f"TaskQueue({len(self._tasks)} tasks)"

    # Ленивые генераторы
    def filter_by_status(self, status: str) -> Generator[Task, None, None]:#фильтр по статусу
        for task in self._tasks:
            if task.status == status:
                yield task #возвращает генератор

    def filter_by_priority(self, min_priority: int) -> Generator[Task, None, None]:#фильтр по приоритету
        for task in self._tasks:
            if task.priority >= min_priority:
                yield task

    def ready_tasks(self) -> Generator[Task, None, None]:#готовые задачи @property из класса Tasks
        for task in self._tasks:
            if task.is_ready:
                yield task