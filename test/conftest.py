from typing import List
import pytest
import datetime

from model.task import Task
from model.quest import Quest


@pytest.fixture
def test_objectives() -> List[Task]:
    return [Task("Trinken", 0.5, datetime.date(2002, 7, 27), datetime.time(23, 59, 59)),
            Task("Essen", 0.5, datetime.date(2003, 8, 28), datetime.time(0, 0, 0)),
            Task("Dach über dem Kopf", 0.5)]

@pytest.fixture
def quest_1(test_objectives: List[Task]) -> Quest:
    return Quest(test_objectives, "Test Quest 1", 0)

@pytest.fixture
def quest_2(test_objectives: List[Task]) -> Quest:
    reversed_objectives = [test_objectives[-1-i] for i in range(len(test_objectives))]
    return Quest(reversed_objectives, "Test Quest 2", 0)

@pytest.fixture
def quest_with_time(test_objectives: List[Task]) -> Quest:
    date = datetime.date(2027, 8, 13)
    time = datetime.time(11, 55, 30)
    return Quest(test_objectives, "Test Quest with time", 0, date, time, 120)