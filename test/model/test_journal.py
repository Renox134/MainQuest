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

        journal_1: Journal = Journal(quests, goals)
        journal_1.export_journal("test/test_journal.json")

        journal_2: Journal = Journal()
        journal_2.import_quests("test/test_journal.json")

        # asser quests are equal
        assert len(journal_2.quests) == len(journal_1.quests)

        for actual_quest, imported_quest in zip(journal_1.quests, journal_2.quests):
            assert actual_quest == imported_quest

        # assert goals are equal
        assert len(journal_2.goals) == len(journal_1.goals)

        for actual_goal, imported_goal in zip(journal_1.goals, journal_2.goals):
            if not actual_goal == imported_goal:
                print("Actual:")
                print(actual_goal)
                print("\nImported")
                print(imported_goal)
            assert actual_goal == imported_goal

    @pytest.mark.parametrize(
            "quest_list, goal_list, transfer_progress, set_to_completed", [
                (["quest_1", "quest_2"], ["goal_1"], True, True),
                (["quest_2", "quest_1"], ["goal_1"], True, True),
                (["quest_2", "quest_1"], ["goal_1"], True, False),
                (["quest_2", "quest_1"], ["goal_1"], False, True),
                ]
    )
    def test_quest_finish(self, quest_list: List[str], goal_list: List[str],
                          transfer_progress: bool,
                          set_to_completed: bool,
                          request: pytest.FixtureRequest):
        quests: List[Quest] = [request.getfixturevalue(q) for q in quest_list]
        to_remove = quests[0]
        goals: List[Goal] = [request.getfixturevalue(g) for g in goal_list]

        journal: Journal = Journal(quests, goals)

        sum_of_tasks = len(to_remove.get_all_tasks())
        sum_of_completed_tasks = sum_of_tasks - len(to_remove.get_all_tasks(False))
        sum_of_progress_dict_before = sum(journal.goals[0].progress_dict.values())

        journal.finish_quest(quests[0], transfer_progress, set_to_completed)

        # check quest removed from quest list
        assert to_remove not in journal.quests

        # check quest removed from goals
        for g in journal.goals:
            assert to_remove not in g.associated_quests

        # check the transfer of completed tasks
        sum_of_progress_dict_after = sum(journal.goals[0].progress_dict.values())
        if transfer_progress:
            if set_to_completed:
                assert sum_of_progress_dict_after == sum_of_progress_dict_before + sum_of_tasks
            else:
                assert sum_of_progress_dict_after == sum_of_progress_dict_before + sum_of_completed_tasks
        else:
            assert sum_of_progress_dict_after == sum_of_progress_dict_before
