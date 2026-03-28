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
        milestones = {}

        # fill quest list
        for q_n in quest_names:
            to_add = ObjectParser.parse_quest(q_n)
            if isinstance(to_add, Quest):
                quests.append(to_add)

        # fill progress dict
        for key, val in data.get("progress_dict", {}).items():
            progress_dict[datetime.strptime(key, Config.get("datetime_format"))] = val

        # fill milestones
        for key, val in data.get("milestones", {}).items():
            milestones[datetime.strptime(key, Config.get("datetime_format"))] = val

        # get time borders
        progress_time_border = data.get("progress_time_border",
                                        datetime.strptime(
                                            Config.get("default_progress_time_border"),
                                            Config.get("datetime_format")))
        if isinstance(progress_time_border, str):
            progress_time_border = datetime.strptime(progress_time_border,
                                                     Config.get("datetime_format"))

        daily_count_border = data.get("daily_count_border",
                                      Config.get("default_daily_count_border"))

        return Goal(data.get("name", ""), quests, progress_dict, milestones,
                    progress_time_border, daily_count_border)

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
                start_of_day = date.replace(hour=0, minute=0, second=0, microsecond=0)
                result[start_of_day] = result.get(start_of_day, 0) + count
            elif date < lower_bound:
                continue
            else:
                week_start =\
                    (date - timedelta(days=date.weekday())).replace(hour=0, minute=0,
                                                                    second=0, microsecond=0)
                # if the week start would be too early, still include the score
                if week_start < lower_bound:
                    week_start = lower_bound
                result[week_start] = result.get(week_start, 0) + count
        return result

    def __init__(self,
                 name: str = "",
                 associated_quests: List[Quest] = [],
                 progress_dict: Dict[datetime, int] = {},
                 milestones: Dict[datetime, str] = {},
                 progress_time_border: datetime =
                 datetime.strptime(Config.get("default_progress_time_border"),
                                   Config.get("datetime_format")),
                 daily_count_border: int = Config.get("default_daily_count_border")):
        """
        Initializes a goal object.
        """
        self.name = name
        self.associated_quests: List[Quest] = associated_quests
        self.progress_dict: Dict[datetime, int] = progress_dict
        self.progress_time_border: datetime = progress_time_border
        self.daily_count_border: int = daily_count_border
        self.milestones: Dict[datetime, str] = milestones

    def move_quest_to_progress(self, quest: Quest) -> None:
        """
        Writes the completion record of the given quest to the progress dict.

        Args:
            quest (Quest): The quest of which to transfer the progress.
        """
        # get progress dict of quest
        quest_progress_dict = quest.get_progress_dict()

        # integrate progress of quest into local progress dict
        for key, val in quest_progress_dict.items():
            current_value = self.progress_dict.get(key, 0)
            if current_value == 0:
                self.progress_dict[key] = val
            else:
                self.progress_dict[key] += val

        # reformat the progress dict
        self.progress_dict = self.format_progress_dict(self.progress_dict, self.daily_count_border,
                                                       self.progress_time_border)

    def get_progress(self) -> Dict[datetime, int]:
        result = self.progress_dict

        # include current progress of associated quests
        for q in self.associated_quests:
            result |= q.get_progress_dict()
            result = self.format_progress_dict(result, self.daily_count_border,
                                               self.progress_time_border)
        return result

    def to_dict(self) -> Dict[str, Any]:
        str_progress_dict = {}
        for key, int_val in self.progress_dict.items():
            str_progress_dict[key.strftime(Config.get("datetime_format"))] = int_val

        str_milestone_dict = {}
        for key, str_val in self.milestones.items():
            str_milestone_dict[key.strftime(Config.get("datetime_format"))] = str_val

        progress_time_border_str =\
            self.progress_time_border.strftime(Config.get("datetime_format"))

        return {
            "name": self.name,
            "quest_names": [q.name for q in self.associated_quests],
            "progress_dict": str_progress_dict,
            "milestones": str_milestone_dict,
            "daily_count_border": self.daily_count_border,
            "progress_time_border": progress_time_border_str
        }

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Goal):
            return False
        return (
            self.name == other.name and
            self.associated_quests == other.associated_quests and
            self.progress_dict == other.progress_dict and
            self.milestones == other.milestones and
            self.daily_count_border == other.daily_count_border and
            self.progress_time_border == other.progress_time_border
        )

    def __str__(self) -> str:
        n = self.name
        aql = f"Associated quests:\t{[q.name for q in self.associated_quests]}"
        progress_count = f"Progress count sum:\t{sum(self.progress_dict.values())}"
        num_milestones = f"Number of milestones:\t{len(self.milestones.values())}"
        daily_border = f"Border for daily progress storing:\t{self.daily_count_border}"
        inclusion_border = "Inclusion border:\t"
        if self.progress_time_border is not None:
            inclusion_border += self.progress_time_border.strftime(Config.get("datetime_format"))
        else:
            inclusion_border += "None"

        return (n + "\n" + aql + "\n" + progress_count + "\n" +
                num_milestones + "\n" + daily_border)
