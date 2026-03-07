from typing import List, Dict, Any

from model.quest import Quest
from object_parser import ObjectParser


class Goal:
    """
    A class representing a long-term goal that the user wants to achieve.
    """

    @staticmethod
    def to_goal(data: Dict[str, Any]) -> "Goal":
        quest_names: List[str] = data.get("quest_names", [])
        quests: List[Quest] = []
        for q_n in quest_names:
            to_add = ObjectParser.parse_quest(q_n)
            if isinstance(to_add, Quest):
                quests.append(to_add)
        return Goal(data.get("name", ""), quests)

    def __init__(self, name: str = "", associated_quests: List[Quest] = []):
        """
        Initializes a goal object.
        """
        self.name = name
        self.associated_quests: List[Quest] = associated_quests

    def add_quest(self, quest: Quest) -> None:
        if quest not in self.associated_quests:
            self.associated_quests.append(quest)

    def remove_quest(self, quest: Quest) -> Quest | None:
        if quest in self.associated_quests:
            return self.associated_quests.pop(self.associated_quests.index(quest))
        else:
            return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "quest_names": [q.name for q in self.associated_quests]
        }
