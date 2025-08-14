from typing import List
import pytest
import datetime

from model.objective import Objective
from model.activity import Activity
from model.quest import Quest


@pytest.fixture
def test_objectives() -> List[Objective]:
    return [Objective("Test objective " + str(i + 1)) for i in range(3)]

@pytest.fixture
def quest_1(test_objectives: List[Objective]) -> Quest:
    return Quest(test_objectives, "Test Quest", 0)

@pytest.fixture
def quest_2(test_objectives: List[Objective]) -> Quest:
    reversed_objectives = [test_objectives[-1-i] for i in range(len(test_objectives))]
    return Quest(reversed_objectives, "Test Quest", 0)

@pytest.fixture
def quest_with_time(test_objectives: List[Objective]) -> Quest:
    date = datetime.date(2027, 8, 13)
    time = datetime.time(11, 55, 30)
    return Quest(test_objectives, "Test Quest", 0, date, time, 120)