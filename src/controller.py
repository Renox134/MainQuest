import json

from typing import List
from model.quest import Quest
from model.goal import Goal


class Controller:
    """
    A class that can hold and manage quests and goals.
    """
    def __init__(self, quests: List[Quest] = [], goals: List[Goal] = []):
        self.quests = quests
        self.goals = goals

    def export_quests(self, path: str) -> None:
        to_export = [q.to_dict() for q in self.quests]

        with open(path, "w") as file:
            json.dump(to_export, file, indent=4, ensure_ascii=False)

    def import_quests(self, path: str) -> None:
        with open(path, "r") as file:
            raw_input = json.load(file)
            for q in raw_input:
                if isinstance(q, dict):
                    self.quests.append(Quest.to_quest(q))
                else:
                    print("WARNING: Non-dict found in quest list")
