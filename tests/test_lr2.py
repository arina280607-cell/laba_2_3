"""
Тесты для лабораторной работы №2
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import pytest
from datetime import datetime
from src.contracts.tasks import Task, PositiveInt, StatusDescriptor


class TestPositiveIntDescriptor:
    """Тесты для дескриптора PositiveInt"""

    def test_valid_values(self):
        """Тест корректных значений"""

        class TestModel:
            value = PositiveInt()

        obj = TestModel()
        obj.value = 1
        assert obj.value == 1

        obj.value = 100
        assert obj.value == 100
        obj.value = 999
        assert obj.value == 999

    def test_invalid_values_raise_error(self):
        """Тест некорректных значений"""

        class TestModel:
            value = PositiveInt()

        obj = TestModel()

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            obj.value = 0

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            obj.value = -5

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            obj.value = -100

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            obj.value = 3.14

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            obj.value = "abc"

    def test_descriptor_via_class(self):
        """Тест доступа к дескриптору через класс"""

        class TestModel:
            value = PositiveInt()

        assert isinstance(TestModel.value, PositiveInt)


class TestStatusDescriptor:
    """Тесты для дескриптора StatusDescriptor"""

    def test_valid_statuses(self):
        """Тест корректных статусов"""

        class TestModel:
            status = StatusDescriptor()

        obj = TestModel()

        obj.status = "new"
        assert obj.status == "new"

        obj.status = "in_progress"
        assert obj.status == "in_progress"

        obj.status = "done"
        assert obj.status == "done"

    def test_invalid_statuses_raise_error(self):
        """Тест некорректных статусов"""

        class TestModel:
            status = StatusDescriptor()

        obj = TestModel()

        invalid_statuses = ["finished", "pending", "closed", "NEW", "DONE", "", None, 123, "inprogress"]

        for status in invalid_statuses:
            with pytest.raises(ValueError, match="Некорректный статус"):
                obj.status = status


class TestTaskCreation:
    """Тесты создания задач"""

    def test_create_valid_task(self):
        """Создание корректной задачи"""
        task = Task(id=1, description="Тестовая задача", priority=5, status="new")

        assert task.id == 1
        assert task.description == "Тестовая задача"
        assert task.priority == 5
        assert task.status == "new"
        assert isinstance(task.created_at, datetime)

    def test_create_task_with_defaults(self):
        """Создание задачи с параметрами по умолчанию"""
        task = Task(id=1, description="Тест")

        assert task.id == 1
        assert task.description == "Тест"
        assert task.priority == 1
        assert task.status == "new"

    def test_create_task_invalid_id(self):
        """Ошибка при некорректном ID"""
        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            Task(id=0, description="Тест")

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            Task(id=-5, description="Тест")

    def test_create_task_invalid_priority(self):
        """Ошибка при некорректном приоритете"""
        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            Task(id=1, description="Тест", priority=0)

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            Task(id=1, description="Тест", priority=-3)

    def test_create_task_invalid_status(self):
        """Ошибка при некорректном статусе"""
        with pytest.raises(ValueError, match="Некорректный статус"):
            Task(id=1, description="Тест", status="finished")

        with pytest.raises(ValueError, match="Некорректный статус"):
            Task(id=1, description="Тест", status="pending")


class TestTaskModification:
    """Тесты изменения атрибутов"""

    def test_modify_id(self):
        """Изменение ID с валидацией"""
        task = Task(id=1, description="Тест")

        task.id = 10
        assert task.id == 10

        task.id = 999
        assert task.id == 999

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            task.id = -1

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            task.id = 0

    def test_modify_priority(self):
        """Изменение приоритета с валидацией"""
        task = Task(id=1, description="Тест", priority=5)

        task.priority = 10
        assert task.priority == 10

        task.priority = 1
        assert task.priority == 1

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            task.priority = 0

        with pytest.raises(ValueError, match="Должно быть положительным целым числом"):
            task.priority = -5

    def test_modify_status(self):
        """Изменение статуса с валидацией"""
        task = Task(id=1, description="Тест", status="new")

        task.status = "in_progress"
        assert task.status == "in_progress"

        task.status = "done"
        assert task.status == "done"

        task.status = "new"
        assert task.status == "new"

        with pytest.raises(ValueError, match="Некорректный статус"):
            task.status = "finished"

    def test_cannot_modify_created_at(self):
        """created_at нельзя изменить (только для чтения)"""
        task = Task(id=1, description="Тест")
        original = task.created_at

        with pytest.raises(AttributeError):
            task.created_at = datetime.now()

        assert task.created_at == original

    def test_description_is_regular_attribute(self):
        """description - обычный атрибут без валидации"""
        task = Task(id=1, description="Тест")

        task.description = "Новое описание"
        assert task.description == "Новое описание"

        task.description = "Любой текст"
        assert task.description == "Любой текст"


class TestTaskProperties:
    """Тесты property-свойств"""

    def test_is_ready_computed_property(self):
        """is_ready вычисляется из статуса"""
        task = Task(id=1, description="Тест", status="new")

        assert task.is_ready is True

        task.status = "in_progress"
        assert task.is_ready is False

        task.status = "done"
        assert task.is_ready is False

        task.status = "new"
        assert task.is_ready is True

    def test_created_at_is_timestamp(self):
        """created_at - это datetime объект"""
        task = Task(id=1, description="Тест")
        assert isinstance(task.created_at, datetime)

    def test_created_at_different_for_different_tasks(self):
        """У разных задач разное время создания"""
        import time
        task1 = Task(id=1, description="Первый")
        time.sleep(0.01)
        task2 = Task(id=2, description="Второй")

        assert task2.created_at > task1.created_at


class TestDataDescriptorPriority:
    """Тесты приоритета data descriptor"""

    def test_cannot_bypass_descriptor_via_dict(self):
        """Нельзя обойти data descriptor через __dict__"""
        task = Task(id=42, description="Тест", priority=10, status="new")

        # Пытаемся обойти
        task.__dict__['id'] = -999
        task.__dict__['priority'] = -100
        task.__dict__['status'] = "finished"

        # Data descriptor имеет приоритет - значения не изменились
        assert task.id == 42
        assert task.priority == 10
        assert task.status == "new"


class TestTaskRepresentation:
    """Тесты строкового представления"""

    def test_repr_format(self):
        """Формат __repr__"""
        task = Task(id=1, description="Тестовая задача", priority=5, status="new")

        repr_str = repr(task)

        assert "Task" in repr_str
        assert "id=1" in repr_str
        assert "description='Тестовая задача'" in repr_str
        assert "priority=5" in repr_str
        assert "status='new'" in repr_str

    def test_repr_changes_after_modification(self):
        """__repr__ обновляется после изменения"""
        task = Task(id=1, description="Тест", priority=1, status="new")

        task.priority = 10
        task.status = "in_progress"

        repr_str = repr(task)
        assert "priority=10" in repr_str
        assert "status='in_progress'" in repr_str


class TestTaskInvariants:
    """Тесты защиты инвариантов"""

    def test_all_invariants_protected(self):
        """Все инварианты защищены"""
        task = Task(id=1, description="Тест", priority=1, status="new")

        # Инвариант 1: id > 0
        with pytest.raises(ValueError):
            task.id = 0
        assert task.id > 0

        # Инвариант 2: priority > 0
        with pytest.raises(ValueError):
            task.priority = 0
        assert task.priority > 0

        # Инвариант 3: status в {new, in_progress, done}
        with pytest.raises(ValueError):
            task.status = "invalid"
        assert task.status in {"new", "in_progress", "done"}

        # Инвариант 4: created_at неизменяем
        with pytest.raises(AttributeError):
            task.created_at = datetime.now()


class TestEdgeCases:
    """Тесты граничных случаев"""

    def test_maximum_values(self):
        """Максимальные значения"""
        task = Task(id=999999, description="Макс ID", priority=999999)
        assert task.id == 999999
        assert task.priority == 999999

    def test_description_long_text(self):
        """Длинное описание"""
        long_text = "A" * 10000
        task = Task(id=1, description=long_text)
        assert task.description == long_text

    def test_status_case_sensitive(self):
        """Статус чувствителен к регистру"""
        task = Task(id=1, description="Тест")

        # Только нижний регистр работает
        with pytest.raises(ValueError):
            task.status = "NEW"

        with pytest.raises(ValueError):
            task.status = "In_Progress"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=src.contracts.tasks", "--cov-report=term-missing"])