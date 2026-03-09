import pytest

from typing import List
from model.quest import Quest
from model.goal import Goal
from journal import Journal

class TestJournal:

    @pytest.mark.parametrize(
            "quest_list, goal_list", [
                (["quest_1", "quest_2", "quest_3"], ["goal_1"]),
                (["quest_2", "quest_1", "quest_3"], ["goal_1"]),
                (["quest_3", "quest_1", "quest_2"], ["goal_1"])
                ]

    )
    def test_io(self, quest_list: List[str], goal_list: List[str], request: pytest.FixtureRequest):
        quests: List[Quest] = [request.getfixturevalue(q) for q in quest_list]
        goals: List[Goal] = [request.getfixturevalue(g) for g in goal_list]

        controller_1: Journal = Journal(quests, goals)
        controller_1.export_journal("test/test_journal.json")

        controller_2: Journal = Journal()
        if len(controller_2.quests):
            controller_2.quests = []

        controller_2.import_quests("test/test_journal.json")

        # asser both logs are equal
        assert len(controller_2.quests) == len(controller_1.quests)

        for el1, el2 in zip(controller_1.quests, controller_2.quests):
            assert el1 == el2
