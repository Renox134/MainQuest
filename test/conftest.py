from typing import List
import pytest
from datetime import date, time

from model.task import Task
from model.quest import Quest


@pytest.fixture
def test_tasks() -> List[Task]:
    """Provides a few example Task objects to be used as Quest tasks."""
    return [
        Task(
            description="Collect water",
            date=date(2002, 7, 27),
            start_time=time(6),
            end_time=(time(8)),
        ),
        Task(
            description="Gather food",
            date=date(2003, 8, 28),
            start_time=time(6),
            end_time=(time(8)),
        ),
        Task(
            description="Build shelter",
            date=None,
        )
    ]


@pytest.fixture
def quest_1(test_tasks: List[Task]) -> Quest:
    """A quest with a straightforward list of tasks."""
    return Quest(name="Test Quest 1", tasks=test_tasks)


@pytest.fixture
def quest_2(test_tasks: List[Task]) -> Quest:
    """A quest with the same tasks in reverse order."""
    reversed_tasks = list(reversed(test_tasks))
    return Quest(name="Test Quest 2", tasks=reversed_tasks)


@pytest.fixture
def quest_with_time(test_tasks: List[Task]) -> Quest:
    """A quest where tasks have due dates around a specific time context."""
    # Optionally modify the tasks for this quest
    adjusted_tasks = [
        Task(
            description=o.description + " (timed)",
            date=date(2027, 8, 13),
        )
        for o in test_tasks
    ]

    return Quest(name="Test Quest with time", tasks=adjusted_tasks)
