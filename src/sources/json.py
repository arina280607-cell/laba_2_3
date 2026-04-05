import json
from typing import Iterable
from pathlib import Path
from src.contracts.task_source import TaskSource
from src.contracts.tasks import Task


class JSONTaskSource:
    """
    Читает задачи из JSONL файла
    """
    name = "file-jsonl"
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_tasks(self) -> Iterable[Task]:#возвращает итерируемый объект, который выдает объекты типа Task
        with open(self.file_path, "r", encoding="utf-8") as f:#гарантирует, что ресурс будет правильно освобожден, даже если произойдет ошибка
            for line in f:
                data = json.loads(line)#Преобразует JSON-строку в словарь
                yield Task(id=data["id"],
                           description=data.get("description", ""),
                           priority=data.get("priority", 1))#Создаёт объект Task и возвращает его