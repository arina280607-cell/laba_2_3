import uuid
from dataclasses import dataclass
from typing import Any

@dataclass(frozen=True, slots=True)
class Task:
    id: str
    payload: Any #так как в условии сказано про произвольные данные задачи
