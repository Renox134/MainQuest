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
