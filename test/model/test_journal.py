import pytest

from typing import List
from model.quest import Quest
from model.goal import Goal
from journal import Journal
from object_parser import ObjectParser


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

        # setup parser
        ObjectParser.init(quests)

        controller_1: Journal = Journal(quests, goals)
        controller_1.export_journal("test/test_journal.json")

        controller_2: Journal = Journal()
        controller_2.import_quests("test/test_journal.json")

        # asser quests are equal
        assert len(controller_2.quests) == len(controller_1.quests)

        for actual_quest, imported_quest in zip(controller_1.quests, controller_2.quests):
            assert actual_quest == imported_quest

        # assert goals are equal
        assert len(controller_2.goals) == len(controller_1.goals)

        for actual_goal, imported_goal in zip(controller_1.goals, controller_2.goals):
            if not actual_goal == imported_goal:
                print("Actual:")
                print(actual_goal)
                print("\nImported")
                print(imported_goal)
            assert actual_goal == imported_goal
