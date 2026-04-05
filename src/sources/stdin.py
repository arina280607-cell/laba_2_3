from typing import Iterable
from src.contracts.tasks import Task
from src.contracts.task_source import TaskSource

class StdinTaskSource:
    """
    Ввод задач вручную
    """
    name = "stdin"
    def get_tasks(self) -> Iterable[Task]:#возвращает итерируемый объект, который выдает объекты типа Task
        print("Введите задачи (id payload), пустая строка — выход:")

        while True:
            line = input("> ")#Ждёт ввод пользователя
            if not line:
                break

            parts = line.split()
            if len(parts) < 2:
                print("Ошибка формата")
                continue

            try:
                id = int(parts[0])
                description = parts[1]
                priority = int(parts[2]) if len(parts) > 2 else 1
                yield Task(id=id,
                           description=description,
                           priority=priority)
            except ValueError:
                print("ID и приоритет должны быть числами")