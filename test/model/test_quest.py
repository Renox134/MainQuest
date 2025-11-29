import pytest
import json

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


    @pytest.mark.parametrize(
            "quest",
            ["quest_1", "quest_2", "quest_with_time"]

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
            q_1: Quest = request.getfixturevalue(quest)

            with open("test/test_quest.json", "r", encoding="utf-8") as file:
                d = json.load(file)
                q_1_import: Quest = Quest.to_quest(d)

            assert q_1 == q_1_import

        except:
            assert False
