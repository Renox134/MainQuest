import pytest
import json

from datetime import datetime

from model.quest import Quest

class TestQuest:

    def test_quest_eq(self, request: pytest.FixtureRequest):
        q_1: Quest = request.getfixturevalue("quest_1")
        q_1_r: Quest = request.getfixturevalue("quest_2")
        q_2: Quest= request.getfixturevalue("quest_3")

        assert q_1 == q_1
        assert not (q_1_r == q_1)
        assert q_2 == q_2
        assert not (q_1 == q_2)


    @pytest.mark.parametrize(
            "quest",
            ["quest_1", "quest_2", "quest_3"]

    )
    def test_io(self, quest: str, request: pytest.FixtureRequest,):
        self.quest_export(request, quest)
        self.quest_import(request, quest)

    def quest_export(self, request: pytest.FixtureRequest, quest: str):
        try:
            q_1: Quest = request.getfixturevalue(quest)
            with open("test/test_quest.json", "w", encoding="utf-8") as file:

                json.dump(q_1.to_dict(), file, indent=4)
        except:
            assert False

    def quest_import(self, request: pytest.FixtureRequest, quest: str):
        try:
            q: Quest = request.getfixturevalue(quest)

            with open("test/test_quest.json", "r", encoding="utf-8") as file:
                d = json.load(file)
                q_import: Quest = Quest.to_quest(d)

            if not q == q_import:
                print("Expected:")
                print(q)
                print("Actual:")
                print(q_import)
            assert q == q_import

        except:
            assert False


    def test_progress_dict(self, request: pytest.FixtureRequest):
        q: Quest = request.getfixturevalue("quest_3")
        expected = request.getfixturevalue("quest_3_progress_dict")

        assert q.get_progress_dict() == expected

    @pytest.mark.parametrize(
            "quest",
            ["quest_1", "quest_2", "quest_3"]

    )
    def test_complete_all_remaining_tasks(self, quest: str, request: pytest.FixtureRequest):
        q: Quest = request.getfixturevalue(quest)
        controll_dict = {}
        tasks = [t for t in q.get_all_tasks()]
        num_uncompleted_before = len(tasks)
        num_completed_before = num_uncompleted_before - len(q.get_all_tasks(False))
        completion_time = datetime.now()
        origin_tasks = tasks.copy()

        for t in tasks:
            controll_dict[t.description] = t.completion_date

        # set to completed
        q.complete_all_tasks(completion_time)

        num_completed_after = len(q.get_all_tasks()) - len(q.get_all_tasks(False))

        assert len(q.tasks) == 0
        assert num_completed_after == num_completed_before + num_uncompleted_before
        assert len(tasks) == len(origin_tasks)
        
        for task, origin_task in zip(tasks, origin_tasks):
            if controll_dict[task.description] is None:
                assert task.completion_date == completion_time
            else:
                assert task.completion_date == origin_task.completion_date
