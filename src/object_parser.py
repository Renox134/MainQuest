from typing import List

from model.quest import Quest


class ObjectParser:
    """
    A parser that can match string inputs to known objects.
    """
    __quest_list: List[Quest] = []

    @staticmethod
    def init(quest_list: List[Quest]) -> None:
        ObjectParser.__quest_list = quest_list

    @staticmethod
    def parse_quest(quest_name: str) -> Quest | None:
        """
        Searches through all quests known to the controller and returns
        the first quest that has the same name as the given name.

        Args:
            quest_name (str): The quest name to look for.

        Returns:
            Quest | None: The quest object with the matching name or None if none was found.
        """
        if ObjectParser.__quest_list is not None:
            for q in ObjectParser.__quest_list:
                if isinstance(q, Quest) and q.name == quest_name:
                    return q
        return None
