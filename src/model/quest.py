from typing import List, Dict, Any

import datetime
from model.objective import Objective

class Quest:
    """
    A class representing a quest. Quest 
    """
    @staticmethod
    def to_quest(data: Dict[str, Any]) -> "Quest":
        """
        Creates a Quest instance from a compatible dictionary.
        """
        # Convert objectives from dicts to Objective objects
        objectives = []
        for obj_data in data.get("Objectives", []):
            if isinstance(obj_data, dict):
                objectives.append(
                    Objective(
                        description=obj_data.get("Description", ""),
                        status=obj_data.get("Status", 0.0)
                    )
                )
            elif isinstance(obj_data, Objective):
                objectives.append(obj_data)
            else:
                raise ValueError(f"Invalid objective type: {type(obj_data)}")

        # Parse date
        date_str = data.get("Date")
        date = None
        if date_str:
            date = datetime.datetime.strptime(date_str, "%d/%m/%Y").date()

        # Parse time
        time_str = data.get("Time")
        time = None
        if time_str:
            time = datetime.datetime.strptime(time_str, "%H:%M:%S").time()

        return Quest(
            objectives=objectives,
            name=data.get("Name", ""),
            status=data.get("Status", 0.0),
            date=date,
            time=time,
            duration=data.get("Duration")
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
        self.duration: int = duration

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
        return {"Name": self.name,
                "Objectives": [o.to_dict() for o in self.objectives],
                "Status": self.status,
                "Date": date,
                "Time": time,
                "Duration": self.duration}

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
