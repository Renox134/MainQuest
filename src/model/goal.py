from typing import List, Dict, Any

from datetime import datetime, timedelta, date

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
        for key, val in data.get("progress_dict", {}).items():
            progress_dict[datetime.strptime(key, Config.get("date_format")).date()] = int(val)

        # get time borders
        progress_time_border = data.get("progress_time_border",
                                        datetime.strptime(
                                            Config.get("default_progress_time_border"),
                                            Config.get("date_format")))
        if isinstance(progress_time_border, str):
            progress_time_border = datetime.strptime(progress_time_border,
                                                     Config.get("date_format")).date()

        daily_count_border = data.get("daily_count_border",
                                      Config.get("default_daily_count_border"))

        return Goal(data.get("name", ""), quests, progress_dict,
                    progress_time_border, daily_count_border)

    @staticmethod
    def format_progress_dict(base: Dict[date, int],
                             daily_border: date | int,
                             lower_bound: date) -> Dict[date, int]:
        result: Dict[date, int] = {}
        daily_count_bound: int | date

        if isinstance(daily_border, int):
            daily_count_bound = (datetime.now() - timedelta(days=daily_border)).date()
        elif isinstance(daily_border, date):
            daily_count_bound = daily_border
        else:
            return result

        for d, count in base.items():
            if d >= daily_count_bound:
                result[d] = result.get(d, 0) + count
            elif d < lower_bound:
                continue
            else:
                week_start =\
                    (d - timedelta(days=d.weekday()))
                # if the week start would be too early, still include the score
                if week_start < lower_bound:
                    week_start = lower_bound
                result[week_start] = result.get(week_start, 0) + count

        # final sort
        result = dict(sorted(result.items()))
        return result

    def __init__(self,
                 name: str = "",
                 associated_quests: List[Quest] = [],
                 progress_dict: Dict[date, int] = {},
                 progress_time_border: date =
                 datetime.strptime(Config.get("default_progress_time_border"),
                                   Config.get("date_format")).date(),
                 daily_count_border: int = Config.get("default_daily_count_border")):
        """
        Initializes a goal object.
        """
        self.name = name
        self.associated_quests: List[Quest] = associated_quests
        self.progress_dict: Dict[date, int] = progress_dict
        self.progress_time_border: date = progress_time_border
        self.daily_count_border: int = daily_count_border

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

    def get_progress(self) -> Dict[date, int]:
        result = self.progress_dict.copy()

        # include current progress of associated quests
        for q in self.associated_quests:
            result |= q.get_progress_dict()
            result = self.format_progress_dict(result, self.daily_count_border,
                                               self.progress_time_border)
        return result

    def to_dict(self) -> Dict[str, Any]:
        str_progress_dict = {}
        for key, int_val in self.progress_dict.items():
            str_progress_dict[key.strftime(Config.get("date_format"))] = int_val

        progress_time_border_str =\
            self.progress_time_border.strftime(Config.get("date_format"))

        return {
            "name": self.name,
            "quest_names": [q.name for q in self.associated_quests],
            "progress_dict": str_progress_dict,
            "daily_count_border": self.daily_count_border,
            "progress_time_border": progress_time_border_str
        }

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Goal):
            return False

        print("Time Border: ", self.progress_time_border, other.progress_time_border)
        return (
            self.name == other.name and
            self.associated_quests == other.associated_quests and
            self.progress_dict == other.progress_dict and
            self.daily_count_border == other.daily_count_border and
            self.progress_time_border == other.progress_time_border
        )

    def __str__(self) -> str:
        n = self.name
        aql = f"Associated quests:\t{[q.name for q in self.associated_quests]}"
        daily_border = f"Border for daily progress storing:\t{self.daily_count_border}"
        inclusion_border = "Inclusion border:\t"
        if self.progress_time_border is not None:
            inclusion_border += self.progress_time_border.strftime(Config.get("date_format"))
        else:
            inclusion_border += "None"

        return (n + "\n" + aql + "\n" + str(self.progress_dict) + "\n" +
                inclusion_border + "\n" + daily_border)
