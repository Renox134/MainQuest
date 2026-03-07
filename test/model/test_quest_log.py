import pytest
import json

from typing import List
from model.quest import Quest
from controller import Controller

class TestQuestLog:

    @pytest.mark.parametrize(
            "quest_list",
            [["quest_1", "quest_2", "quest_with_time"],
             ["quest_2", "quest_1", "quest_with_time"],
             ["quest_with_time", "quest_1", "quest_2"]]

    )
    def test_io(self, quest_list: List[str], request: pytest.FixtureRequest):
        quests: List[Quest] = [request.getfixturevalue(q) for q in quest_list]
        controller_1: Controller = Controller(quests)
        controller_1.export_quests("test/test_quest_log.json")

        controller_2: Controller = Controller()
        if len(controller_2.quests):
            controller_2.quests = []

        controller_2.import_quests("test/test_quest_log.json")

        # asser both logs are equal
        assert len(controller_2.quests) == len(controller_1.quests)

        for el1, el2 in zip(controller_1.quests, controller_2.quests):
            assert el1 == el2
