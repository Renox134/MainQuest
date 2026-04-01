from typing import Dict

from config_reader import Config

from datetime import datetime


class Milestone:
    @staticmethod
    def to_milestone(data: Dict[str, str]) -> "Milestone":
        return Milestone(
            data.get("name", ""),
            datetime.strptime(data.get("datetime", "01/01/2026, 00:00"),
                              Config.get("datetime_format")),
            data.get("type", "")
        )

    def __init__(self, name: str, datetime: datetime, type: str):
        self.name = name
        self.datetime = datetime
        self.type = type

    def to_dict(self) -> Dict[str, str]:
        return {
            "name": self.name,
            "datetime": self.datetime.strftime(Config.get("datetime_format")),
            "type": self.type
        }
