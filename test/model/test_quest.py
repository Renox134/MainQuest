import pytest
import json

from model.objective import Objective
from model.activity import Activity
from model.quest import Quest

class TestQuest:

    def test_quest_eq(self, request: pytest.FixtureRequest):
        q_1: Quest = request.getfixturevalue("quest_1")
        q_1_r: Quest = request.getfixturevalue("quest_2")
        q_2: Quest= request.getfixturevalue("quest_with_time")

        assert q_1 == q_1
        assert not (q_1_r == q_1)
        assert q_2 == q_2
        assert not (q_1 == q_2)

    def test_quest_export(self, request: pytest.FixtureRequest):
        try:
            q_1: Quest = request.getfixturevalue("quest_1")
            q_1_r: Quest = request.getfixturevalue("quest_2")
            q_2: Quest= request.getfixturevalue("quest_with_time")

            with open("test_quest_log.json", "w", encoding="utf-8") as file:
                json.dump(q_1.to_dict(), file, indent=4)
        except:
            assert False