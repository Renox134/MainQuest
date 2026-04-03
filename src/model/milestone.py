from typing import Dict

from config_reader import Config

from datetime import datetime, date


class Milestone:
    @staticmethod
    def to_milestone(data: Dict[str, str]) -> "Milestone":
        return Milestone(
            data.get("name", ""),
            datetime.strptime(data.get("datetime", Config.get("default_progress_time_border")),
                              Config.get("date_format")),
            data.get("type", "")
        )

    def __init__(self, name: str, date: date, type: str):
        self.name = name
        self.datetime = date
        self.type = type

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "datetime": self.datetime.strftime(Config.get("date_format")),
            "type": self.type
        }
