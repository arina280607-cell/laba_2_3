import json
from typing import Iterable
from pathlib import Path

from src.contracts.tasks import Task


class JSONTaskSource:
    """
    Читает задачи из JSONL файла
    """

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def get_tasks(self) -> Iterable[Task]:
        with open(self.file_path, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line)
                yield Task(id=data["id"], description=data.get("description", ""), priority=data.get("priority", 1))