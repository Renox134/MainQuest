from typing import List, Dict, Any

import datetime
from model.objective import Objective


class Quest:
    """
    A class representing a quest.
    """
    @staticmethod
    def to_quest(data: Dict[str, Any]) -> "Quest":
        """
        Creates a Quest instance from a compatible dictionary.
        """
        # Convert objectives from dicts to Objective objects
        objectives = []
        for obj_data in data.get("objectives", []):
            if isinstance(obj_data, dict):
                objectives.append(Objective.to_objective(obj_data))
            else:
                raise ValueError(f"Invalid objective type: {type(obj_data)}")

        # Parse date
        date_str = data.get("date")
        date = None
        if date_str:
            date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

        # Parse time
        time_str = data.get("time")
        time = None
        if time_str:
            time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()

        return Quest(
            objectives=objectives,
            name=data.get("name", ""),
            status=data.get("status", 0.0),
            date=date,
            time=time,
            duration=data.get("duration", 0)
        )

    def __init__(self, objectives: List[Objective], name: str, status: float = 0,
                 date: datetime.date | None = None,
                 time: datetime.time | None = None, duration: int | None = None):
        """
        Initializes a quest.

        Parameters:
            objectives (List[Objective]): The objectives of this quest.
            name (str): The quest name.
            status (float): The quest status.
            date (datetime.date): Optional var for the date on which the quest takes place.
            time (datetime.time): Optional var for the time at which the quest takes place.
            duration (int): Optional var for the duration (in minutes) that the quest takes.
        """

        self.objectives: List[Objective] = objectives
        self.name: str = name
        self.status = status
        self.date: datetime.date | None = date
        self.time: datetime.time | None = time
        self.duration: int | None = duration

    def add_objective(self, objective: Objective) -> None:
        self.objectives.append(objective)

    def remove_objective(self, idx: int) -> Objective:
        return self.objectives.pop(idx)

    def update_status(self) -> None:
        count = 0
        progress = 0.0
        for obj in self.objectives:
            progress += obj.status
            count += 1
        self.status = round(progress / count, 2)

    def set_status(self, status: float) -> None:
        self.status = status

    def __str__(self) -> str:
        name = "\nName: \t\t" + self.name + "\n"
        obj = "Objectives:\n"
        for i, o in enumerate(self.objectives):
            obj += "\t" + str(o)
            if (i == len(self.objectives) - 1):
                obj += "\n"
        date = ""
        time = ""
        dur = ""
        if self.date is not None:
            date = "Date: \t\t" + self.date.strftime("%d/%m/%Y") + "\n"
        if self.time is not None:
            time = "Time: \t\t" + self.time.strftime("%H:%M:%S") + "\n"
        if self.duration is not None:
            dur = "Duration:\t" + str(self.duration) + "\n"
        return name + obj + date + time + dur

    def to_dict(self) -> Dict[str, Any]:
        date = None
        if self.date is not None:
            date = self.date.strftime("%d/%m/%Y")

        time = None
        if self.time is not None:
            time = self.time.strftime("%H:%M:%S")
        return {"name": self.name,
                "objectives": [o.to_dict() for o in self.objectives],
                "status": self.status,
                "date": date,
                "time": time,
                "duration": self.duration}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Quest):
            return NotImplemented
        return (
            self.name == other.name
            and [obj for obj in self.objectives] == [obj for obj in other.objectives]
            and round(self.status, 2) == round(other.status, 2)
            and self.date == other.date
            and self.time == other.time
            and self.duration == other.duration
        )
