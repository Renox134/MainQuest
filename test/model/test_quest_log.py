import pytest
import json

from typing import List
from model.quest import Quest
from model.quest_log import QuestLog

class TestQuestLog:

    @pytest.mark.parametrize(
            "quest_list",
            [["quest_1", "quest_2", "quest_with_time"],
             ["quest_2", "quest_1", "quest_with_time"],
             ["quest_with_time", "quest_1", "quest_2"]]

    )
    def test_io(self, quest_list: List[str], request: pytest.FixtureRequest):
        quests: List[Quest] = [request.getfixturevalue(q) for q in quest_list]
        log_1: QuestLog = QuestLog(quests)
        log_1.export_quests("test/test_quest_log.json")

        log_2: QuestLog = QuestLog()
        if len(log_2.quests):
            log_2.quests = []

        log_2.import_quests("test/test_quest_log.json")

        # asser both logs are equal
        assert len(log_2.quests) == len(log_1.quests)

        for el1, el2 in zip(log_1.quests, log_2.quests):
            assert el1 == el2
