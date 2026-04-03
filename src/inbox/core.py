from typing import List
from src.contracts.task_source import TaskSource
from src.contracts.tasks import Task


class InboxApp:
    """
    Основное приложение
    """

    def __init__(self):
        self.tasks: List[Task] = []

    def load_tasks(self, source: TaskSource):
        # runtime проверка Protocol
        if not isinstance(source, TaskSource):
            raise TypeError("Источник не реализует TaskSource")

        for task in source.get_tasks():
            self.tasks.append(task)

    def show_tasks(self):
        for task in self.tasks:
            print(task)