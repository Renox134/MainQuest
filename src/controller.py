import json

from typing import List
from model.quest import Quest


class Controller:
    """
    A class that can hold and manage quests and goals.
    """
    def __init__(self, quests: List[Quest] = []):
        self.quests = quests
        self.completed_quests: List[Quest] = []

    def toggle_quest(self, to_toggle: Quest) -> None:
        """
        Toggles the completion of the given quest.
        """
        if to_toggle in self.quests:
            self.quests.remove(to_toggle)
            self.completed_quests.append(to_toggle)
        elif to_toggle in self.completed_quests:
            self.completed_quests.remove(to_toggle)
            self.quests.append(to_toggle)

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
