from typing import List, Dict, Any

from datetime import datetime, timedelta

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

        # fill milestones
        for key, val in data.get("milestones", {}):
            progress_dict[datetime.strptime(key, Config.get("datetime_format"))] = val

        return Goal(data.get("name", ""), quests, progress_dict)

    @staticmethod
    def format_progress_dict(base: Dict[datetime, int],
                             daily_border: datetime | int,
                             lower_bound: datetime) -> Dict[datetime, int]:
        result: Dict[datetime, int] = {}
        daily_count_bound: int | datetime

        if isinstance(daily_border, int):
            daily_count_bound = datetime.now() - timedelta(days=daily_border)
        elif isinstance(daily_border, datetime):
            daily_count_bound = daily_border
        else:
            return result

        for date, count in base.items():
            if date >= daily_count_bound:
                start_of_day = date.replace(hour=0, minute=0, second=0)
                result[start_of_day] = result.get(start_of_day, 0) + count
            elif date < lower_bound:
                continue
            else:
                week_start =\
                    (date - timedelta(days=date.weekday())).replace(hour=0, minute=0, second=0)
                # if the week start would be too early, still include the score
                if week_start < lower_bound:
                    week_start = lower_bound
                result[week_start] = result.get(week_start, 0) + count
        return result

    def __init__(self, name: str = "", associated_quests: List[Quest] = [],
                 progress_dict: Dict[datetime, int] = {},
                 milestones: Dict[datetime, str] = {},
                 progress_time_border: datetime = datetime(2026, 1, 1),
                 daily_count_border: int = 30):
        """
        Initializes a goal object.
        """
        self.name = name
        self.associated_quests: List[Quest] = associated_quests
        self.progress_dict: Dict[datetime, int] = progress_dict
        self.progress_time_border: datetime = progress_time_border
        self.daily_count_border: int = daily_count_border
        self.milestones: Dict[datetime, str] = milestones

    def add_quest(self, quest: Quest) -> None:
        if quest not in self.associated_quests:
            self.associated_quests.append(quest)

    def remove_quest(self, quest: Quest) -> Quest | None:
        if quest in self.associated_quests:
            return self.associated_quests.pop(self.associated_quests.index(quest))
        else:
            return None

    def move_quest_to_progress(self, quest: Quest) -> None:
        """
        Removes a qiven quest from the associated quests and writes the completion record
        of the quest to the progress dict.

        Args:
            quest (Quest): The quest of which to transfer the progress.
        """
        # get progress dict of quest
        quest_progress_dict = quest.get_progress_dict()

        # integrate progress of quest into local progress dict
        self.progress_dict |= quest_progress_dict

        # reformat the progress dict
        self.progress_dict = self.format_progress_dict(self.progress_dict, self.daily_count_border,
                                                       self.progress_time_border)

        # remove quest from associated quests
        self.remove_quest(quest)

    def to_dict(self) -> Dict[str, Any]:
        str_progress_dict = {}
        for key, int_val in self.progress_dict.items():
            str_progress_dict[key.strftime(Config.get("datetime_format"))] = int_val

        str_milestone_dict = {}
        for key, str_val in self.milestones.items():
            str_milestone_dict[key.strftime(Config.get("datetime_format"))] = str_val

        return {
            "name": self.name,
            "quest_names": [q.name for q in self.associated_quests],
            "progress_dict": str_progress_dict,
            "milestones": str_milestone_dict
        }
