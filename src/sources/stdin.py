from typing import Iterable
from src.contracts.tasks import Task


class StdinTaskSource:
    """
    Ввод задач вручную
    """

    def get_tasks(self) -> Iterable[Task]:
        print("Введите задачи (id payload), пустая строка — выход:")

        while True:
            line = input("> ")
            if not line:
                break

            parts = line.split(maxsplit=1)
            if len(parts) < 2:
                print("Ошибка формата")
                continue

            try:
                id = int(parts[0])
                description = parts[1]
                priority = int(parts[2]) if len(parts) > 2 else 1
                yield Task(id=id, description=description, priority=priority)
            except ValueError:
                print("ID и приоритет должны быть числами")