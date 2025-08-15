import json

from typing import List
from model.quest import Quest


class QuestLog:
    """
    A class that can hold and manage quests.
    """
    def __init__(self, quests: List[Quest] = []):
        self.__quests = quests

    def get_quests(self) -> List[Quest]:
        return self.__quests

    def add_quest(self, quest: Quest) -> None:
        self.__quests.append(quest)

    def remove_quest(self, idx: int) -> Quest:
        return self.__quests.pop(idx)

    def clear_quests(self) -> None:
        self.__quests = []

    def export_quests(self, path: str) -> None:
        to_export = [q.to_dict() for q in self.__quests]

        with open(path, "w") as file:
            json.dump(to_export, file, indent=4, ensure_ascii=False)

    def import_quests(self, path: str) -> None:
        with open(path, "r") as file:
            raw_input = json.load(file)
            for q in raw_input:
                if isinstance(q, dict):
                    self.__quests.append(Quest.to_quest(q))
                else:
                    print("WARNING: Non-dict found in quest list")
