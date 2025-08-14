import json

from model.objective import Objective
from model.quest import Quest
from model.quest_log import QuestLog

from gui.quest_app import QuestApp


if __name__ == "__main__":
    quest_dict = {}
    with open("main_quest.json", "r") as file:
        quest_dict = json.load(file)

    q = Quest.to_quest(quest_dict)
    ql: QuestLog = QuestLog([q])

    QuestApp(ql).run()
