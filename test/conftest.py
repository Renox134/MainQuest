from typing import List
import pytest
import datetime

from model.task import Task
from model.quest import Quest


@pytest.fixture
def test_tasks() -> List[Task]:
    """Provides a few example Task objects to be used as Quest tasks."""
    return [
        Task(
            description="Collect water",
            duedate=datetime.datetime(2002, 7, 27, 23, 59, 59),
            duration=30
        ),
        Task(
            description="Gather food",
            duedate=datetime.datetime(2003, 8, 28, 0, 0, 0),
            duration=45
        ),
        Task(
            description="Build shelter",
            duedate=None,
            duration=120
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
            duedate=datetime.datetime(2027, 8, 13, 11, 55, 30),
            duration=o.duration
        )
        for o in test_tasks
    ]

    return Quest(name="Test Quest with time", tasks=adjusted_tasks)
