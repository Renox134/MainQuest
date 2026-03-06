from typing import List, Dict, Any

from model.quest import Quest


class Goal:
    """
    A class representing a long-term goal that the user wants to achieve.
    """

    @staticmethod
    def to_goal(data: Dict[str, Any]) -> "Goal":
        return Goal(data.get("title", ""))

    def __init__(self, title: str = ""):
        """
        Initializes a goal object.
        """
        self.title = title
        self.associated_quests: List[Quest] = []

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
            "title": self.title
        }
