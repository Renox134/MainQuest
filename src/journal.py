import json

from datetime import datetime

from typing import List
from model.quest import Quest
from model.goal import Goal
from model.milestone import Milestone
from object_parser import ObjectParser


class Journal:
    """
    A class that can hold and manage quests and goals.
    """
    def __init__(self, quests: List[Quest] = [], goals: List[Goal] = [],
                 milestones: List[Milestone] = []):
        self.quests = quests
        self.goals = goals
        self.milestones = milestones

    def finish_quest(self, quest: Quest,
                     transfer_progress: bool = True,
                     set_to_completed: bool = True) -> None:

        if set_to_completed:
            # complete all potentially uncompleted tasks
            quest.complete_all_tasks(datetime.now())

        # make sure the goals update the progress dict when enabled
        if transfer_progress:
            for goal in self.goals:
                if quest in goal.associated_quests:
                    goal.move_quest_to_progress(quest)
            self.milestones.append(Milestone(quest.name, datetime.now(), "quest"))

        # remove quest from all goals
        for goal in self.goals:
            if quest in goal.associated_quests:
                goal.associated_quests.remove(quest)

        # remove quest from quest list
        self.quests.remove(quest)

    def finish_goal(self, goal: Goal, move_to_milestone: bool) -> None:
        if move_to_milestone:
            self.milestones.append(Milestone(goal.name, datetime.now(), "goal"))
        # remove goal
        self.goals.remove(goal)

    def export_journal(self, path: str) -> None:
        quest_dicts = [q.to_dict() for q in self.quests]
        goal_dicts = [g.to_dict() for g in self.goals]
        milestone_dicts = [m.to_dict() for m in self.milestones]

        to_export = {
            "quests": quest_dicts,
            "goals": goal_dicts,
            "milestones": milestone_dicts
        }

        with open(path, "w") as file:
            json.dump(to_export, file, indent=4, ensure_ascii=False)

    def import_journal(self, path: str) -> None:
        # clear out everything old
        self.quests = []
        self.goals = []
        self.milestones = []

        with open(path, "r") as file:
            raw_input = json.load(file)
            if isinstance(raw_input, dict):
                quest_dicts = raw_input.get("quests", [])
                goal_dicts = raw_input.get("goals", [])
                milestone_dicts = raw_input.get("milestones", [])

                # add quests
                for q in quest_dicts:
                    if isinstance(q, dict):
                        self.quests.append(Quest.to_quest(q))
                    else:
                        print("WARNING: Non-dict found in quest list")
                # init quest parser
                parser = ObjectParser()
                parser.init(self.quests)
                # add goals
                for g in goal_dicts:
                    if isinstance(g, dict):
                        self.goals.append(Goal.to_goal(g))
                    else:
                        print("WARNING: Non-dict found in goal list")
                # add milestones
                for m in milestone_dicts:
                    if isinstance(m, dict):
                        self.milestones.append(Milestone.to_milestone(m))
                    else:
                        print("WARNING: Non-dict found in milestone list")
