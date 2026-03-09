from typing import List
import pytest
from datetime import date, time, datetime

from model.task import Task
from model.quest import Quest
from model.goal import Goal


@pytest.fixture
def test_tasks() -> List[Task]:
    """Provides a few example Task objects to be used as Quest tasks."""
    return [
        Task(
            description="Collect water",
            date=date(2024, 2, 27),
            start_time=time(6),
            end_time=(time(18)),
            subtasks=[
                Task(
                    "Build rain collector",
                    date=date(2024, 2, 27),
                    start_time=time(9),
                    end_time=(time(10)),
                ),
                Task(
                    "Build container for collected water.",
                    date=date(2024, 2, 27),
                    start_time=time(6),
                    end_time=(time(8)),
                    subtasks=[
                        Task(
                            "Look for big leafs."
                        ),
                        Task(
                            "Look for useful wood."
                        )
                    ]
                )
            ]
        ),
        Task(
            description="Gather food",
            date=date(2023, 8, 28),
            start_time=time(6),
            end_time=(time(8)),
        ),
        Task(
            description="Build shelter"
        )
    ]


@pytest.fixture
def completed_test_tasks() -> List[Task]:
    """Provides a few example Task objects to be used as Quest tasks."""
    return [
        Task(
            description="Collect water",
            date=date(2024, 2, 27),
            start_time=time(6),
            end_time=(time(18)),
            completion_date=datetime(2024, 2, 27, 17, 50),
            subtasks=[
                Task(
                    "Build rain collector",
                    date=date(2024, 2, 27),
                    start_time=time(9),
                    end_time=(time(10)),
                    completion_date=datetime(2024, 2, 27, 9, 50)
                ),
                Task(
                    "Build container for collected water.",
                    date=date(2024, 2, 27),
                    start_time=time(6),
                    end_time=(time(8)),
                    completion_date=datetime(2024, 2, 27, 6, 50),
                    subtasks=[
                        Task(
                            "Look for big leafs.",
                            completion_date=datetime(2024, 2, 27, 6, 45),
                        ),
                        Task(
                            "Look for useful wood.",
                            completion_date=datetime(2024, 2, 27, 6, 45),
                        )
                    ]
                )
            ]
        ),
        Task(
            description="Gather food",
            date=date(2024, 2, 22),
            start_time=time(6),
            end_time=(time(8)),
            completion_date=datetime(2024, 2, 22, 6, 50),
        ),
        Task(
            description="Build shelter"
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
def quest_3(completed_test_tasks: List[Task]) -> Quest:
    """A quest with the same tasks in reverse order."""
    return Quest(name="Test Quest 3", tasks=completed_test_tasks)


@pytest.fixture
def goal_1(quest_1: Quest, quest_2: Quest, formated_progress_dict,
           lower_bound, daily_border) -> Goal:
    return Goal("Goal_1", [quest_1, quest_2], formated_progress_dict, {}, lower_bound,
                daily_border)


@pytest.fixture
def quest_3_progress_dict():
    return {
        datetime(2024, 2, 27, 17, 50): 1,
        datetime(2024, 2, 27, 9, 50): 1,
        datetime(2024, 2, 27, 6, 50): 1,
        datetime(2024, 2, 27, 6, 45): 2,
        datetime(2024, 2, 22, 6, 50): 1
    }

@pytest.fixture
def lower_bound():
    return datetime(2024, 1, 10, 0, 0, 0)


@pytest.fixture
def daily_border():
    return datetime(2024, 2, 1, 0, 0, 0)


@pytest.fixture
def unformated_progress_dict():
    return {
        # before lower_bound -> ignored
        datetime(2024, 1, 5, 10, 0): 3,

        # between lower_bound and daily_border -> weekly aggregation
        datetime(2024, 1, 10, 9, 0): 2,
        datetime(2024, 1, 11, 14, 0): 4,
        datetime(2024, 1, 15, 16, 0): 5,
        datetime(2024, 1, 17, 11, 0): 1,

        # after daily_border -> daily aggregation
        datetime(2024, 2, 2, 8, 30): 2,
        datetime(2024, 2, 2, 18, 0): 3,
        datetime(2024, 2, 3, 9, 15): 4,
    }


@pytest.fixture
def formated_progress_dict():
    return {
        # week start would be 2024-01-08 but gets clamped to lower_bound
        datetime(2024, 1, 10, 0, 0): 6,  # 2 + 4

        # normal weekly aggregation
        datetime(2024, 1, 15, 0, 0): 6,  # 5 + 1

        # daily aggregation
        datetime(2024, 2, 2, 0, 0): 5,   # 2 + 3
        datetime(2024, 2, 3, 0, 0): 4,
    }


@pytest.fixture
def fused_progress_dict():
    return {
        datetime(2024, 1, 10, 0, 0): 6,
        datetime(2024, 1, 15, 0, 0): 6,
        datetime(2024, 2, 2, 0, 0): 5,
        datetime(2024, 2, 3, 0, 0): 4,
        datetime(2024, 2, 22, 0, 0): 1,
        datetime(2024, 2, 27, 0, 0): 5,
    }
