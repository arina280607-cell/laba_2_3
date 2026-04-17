import sys
import os
import pytest
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.contracts.tasks import Task
from src.inbox.queue import TaskQueue


@pytest.fixture
def sample_tasks():
    """Тестовые данные для проверки коллекции."""
    return [
        Task(id=1, description="Low priority", priority=1, status="new"),
        Task(id=2, description="High priority", priority=10, status="new"),
        Task(id=3, description="Done task", priority=5, status="done"),
    ]


class TestTaskQueueLR3:
    def test_len_protocol(self, sample_tasks):
        """Проверка работы len(queue) через __len__."""
        queue = TaskQueue(sample_tasks)
        assert len(queue) == 3

    def test_iteration_protocol(self, sample_tasks):
        """Проверка работы цикла for через __iter__."""
        queue = TaskQueue(sample_tasks)
        iterated_ids = [task.id for task in queue]
        assert iterated_ids == [1, 2, 3]

    def test_repeatable_iteration(self, sample_tasks):
        """Проверка, что коллекция не 'одноразовая'."""
        queue = TaskQueue(sample_tasks)
        first_pass = list(queue)
        second_pass = list(queue)
        assert first_pass == second_pass
        assert len(first_pass) == 3

    def test_filter_status_is_lazy(self, sample_tasks):
        """Проверка ленивой фильтрации (генератор)."""
        queue = TaskQueue(sample_tasks)
        gen = queue.filter_by_status("new")

        assert hasattr(gen, "__next__")
        results = list(gen)
        assert len(results) == 2
        assert all(t.status == "new" for t in results)

    def test_filter_priority_is_lazy(self, sample_tasks):
        """Проверка фильтрации по приоритету."""
        queue = TaskQueue(sample_tasks)
        gen = queue.filter_by_priority(5)


        assert hasattr(gen, "__next__")
        results = list(gen)
        assert len(results) == 2