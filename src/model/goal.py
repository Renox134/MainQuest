from typing import List, Dict, Any

from datetime import datetime

from model.quest import Quest
from object_parser import ObjectParser
from config_reader import Config


class Goal:
    """
    A class representing a long-term goal that the user wants to achieve.
    """

    @staticmethod
    def to_goal(data: Dict[str, Any]) -> "Goal":
        quest_names: List[str] = data.get("quest_names", [])
        quests: List[Quest] = []
        progress_dict = {}

        # fill quest list
        for q_n in quest_names:
            to_add = ObjectParser.parse_quest(q_n)
            if isinstance(to_add, Quest):
                quests.append(to_add)

        # fill progress dict
        for key, val in data.get("progress_dict", {}):
            progress_dict[datetime.strptime(key, Config.get("datetime_format"))] = val

        return Goal(data.get("name", ""), quests, progress_dict)

    def __init__(self, name: str = "", associated_quests: List[Quest] = [],
                 progress_dict: Dict[datetime, int] = {}):
        """
        Initializes a goal object.
        """
        self.name = name
        self.associated_quests: List[Quest] = associated_quests
        self.progress_dict: Dict[datetime, int] = progress_dict

    def add_quest(self, quest: Quest) -> None:
        if quest not in self.associated_quests:
            self.associated_quests.append(quest)

    def remove_quest(self, quest: Quest) -> Quest | None:
        if quest in self.associated_quests:
            return self.associated_quests.pop(self.associated_quests.index(quest))
        else:
            return None

    def to_dict(self) -> Dict[str, Any]:
        str_progress_dict = {}
        for key, val in self.progress_dict.items():
            str_progress_dict[key.strftime(Config.get("datetime_format"))] = val

        return {
            "name": self.name,
            "quest_names": [q.name for q in self.associated_quests],
            "progress_dict": str_progress_dict
        }
