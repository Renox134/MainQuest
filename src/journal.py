import json

from typing import List
from model.quest import Quest
from model.goal import Goal


class Journal:
    """
    A class that can hold and manage quests and goals.
    """
    def __init__(self, quests: List[Quest] = [], goals: List[Goal] = []):
        self.quests = quests
        self.goals = goals

    def export_journal(self, path: str) -> None:
        quest_dicts = [q.to_dict() for q in self.quests]
        goal_dicts = [g.to_dict() for g in self.goals]

        to_export = {
            "quests": quest_dicts,
            "goals": goal_dicts
        }

        with open(path, "w") as file:
            json.dump(to_export, file, indent=4, ensure_ascii=False)

    def import_quests(self, path: str) -> None:
        # clear out everything old
        self.quests = []
        self.goals = []

        with open(path, "r") as file:
            raw_input = json.load(file)
            # add quests
            if isinstance(raw_input, dict):
                quest_dicts = raw_input.get("quests", [])
                goal_dicts = raw_input.get("goals", [])

                for q in quest_dicts:
                    if isinstance(q, dict):
                        self.quests.append(Quest.to_quest(q))
                    else:
                        print("WARNING: Non-dict found in quest list")

                for g in goal_dicts:
                    if isinstance(g, dict):
                        self.goals.append(Goal.to_goal(g))
                    else:
                        print("WARNING: Non-dict found in quest list")
