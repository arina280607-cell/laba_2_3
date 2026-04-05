from datetime import datetime


class PositiveInt:#проверяет, что число положительное
    """Data descriptor для положительных целых чисел."""
    def __set_name__(self, owner, name):#получает имя атрибута в классе
        self.name = f"_{name}"#Создаёт скрытое имя для хранения значения

    def __get__(self, obj, objtype=None):
        if obj is None:#если обращаемся к атрибуту через класс, а не через экземпляр
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):#Вызывается при присваивании атрибута
        if not isinstance(value, int) or value <= 0:
            raise ValueError("Должно быть положительным целым числом")
        setattr(obj, self.name, value)#Сохраняет значение в скрытый атрибут


class StatusDescriptor:
    """Data descriptor для статуса задачи."""
    ALLOWED = {"new", "in_progress", "done"}

    def __set_name__(self, owner, name):
        self.name = f"_{name}"#Создаёт скрытое имя для хранения значения (по сути не имеет смысла)

    def __get__(self, obj, objtype=None):
        if obj is None:#если обращаемся к атрибуту через класс, а не через экземпляр
            return self
        return getattr(obj, self.name)

    def __set__(self, obj, value):
        if value not in self.ALLOWED:
            raise ValueError(f"Некорректный статус. Допустимы: {self.ALLOWED}")
        setattr(obj, self.name, value)


class DescriptionDescriptor:
    """Non-data descriptor для описания с проверкой длины."""

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, "")

    def __set__(self, obj, value):
        if not isinstance(value, str):
            raise TypeError("Описание должно быть строкой")
        setattr(obj, self.name, value)


class Task:
    """Модель задачи с дескрипторами и property."""
    id = PositiveInt()
    priority = PositiveInt()
    status = StatusDescriptor()
    description = DescriptionDescriptor()

    def __init__(self, id: int, description: str, priority: int = 1, status: str = "new"):
        self.id = id #Вызывается PositiveInt.__set__(self, task, id) с проверкой
        self.description = description#Вызывается DescriptionDescriptor.__set__ с проверкой
        self.priority = priority#Вызывается PositiveInt.__set__ с проверкой
        self.status = status#Вызывается StatusDescriptor.__set__ с проверкой
        self._created_at = datetime.now()

    @property#Декоратор, превращающий метод в атрибут, non-data дескриптор(Только __get__, нет __set__)
    def created_at(self):
        return self._created_at#получаем значение, но не можем его изменить

    @property
    def is_ready(self) -> bool:#свойство нигде не хранится. Оно вычисляется каждый раз при обращении.
        return self.status == "new"

    def __repr__(self):#строковое представление объекта

        return f"Task(id={self.id}, description='{self.description}', priority={self.priority}, status='{self.status}')"