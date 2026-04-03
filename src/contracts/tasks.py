from datetime import datetime


class PositiveInt:
    """Data descriptor для положительных целых чисел."""
    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Должно быть положительным целым числом")
        setattr(obj, self.name, value)


class StatusDescriptor:
    """Data descriptor для статуса задачи."""
    ALLOWED = {"new", "in_progress", "done"}

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if value not in self.ALLOWED:
            raise ValueError(f"Некорректный статус. Допустимы: {self.ALLOWED}")
        setattr(obj, self.name, value)


class Task:
    """Модель задачи с дескрипторами и property."""
    id = PositiveInt()
    priority = PositiveInt()
    status = StatusDescriptor()

    def __init__(self, id: int, description: str, priority: int = 1, status: str = "new"):
        self.id = id
        self.description = description
        self.priority = priority
        self.status = status
        self._created_at = datetime.now()

    @property
    def created_at(self):
        return self._created_at

    @property
    def is_ready(self) -> bool:
        return self.status == "new"

    def __repr__(self):
        return f"Task(id={self.id}, description='{self.description}', priority={self.priority}, status='{self.status}')"