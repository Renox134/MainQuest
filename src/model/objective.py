from typing import Dict, Any
import datetime


class Objective:

    @staticmethod
    def to_objective(data: Dict[str, Any]) -> "Objective":
        """
        Creates a Quest instance from a compatible dictionary.
        """
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

        return Objective(data.get("description", ""),
                         data.get("status", 0.0),
                         date, time, data.get("duration", 0))

    """
    A class representing an objective that is to be completed.
    """
    def __init__(self, description: str, status: float = 0.0,
                 date: datetime.date | None = None,
                 time: datetime.time | None = None,
                 duration: int | None = None):
        """
        Initializes an objective.

        Parameters:
            description (str): The desription that explaines what the objective is.
            status (float): The objective status.
            date (datetime.date): Optional var for the date on which the objective takes place.
            time (datetime.time): Optional var for the time at which the objective takes place.
            duration (int): Optional var for the duration (in minutes) that the objective takes.
        """
        self.description: str = description
        self.status: float = status
        self.date: datetime.date | None = date
        self.time: datetime.time | None = time
        self.duration: int | None = duration

    def set_status(self, status: float) -> None:
        self.status = status

    def __str__(self) -> str:
        description = "\nDescription: \t\t" + self.description + "\n"
        status = "Status: \t\t" + str(self.status) + "\n"
        date = ""
        time = ""
        dur = ""
        if self.date is not None:
            date = "Date: \t\t" + self.date.strftime("%d/%m/%Y") + "\n"
        if self.time is not None:
            time = "Time: \t\t" + self.time.strftime("%H:%M:%S") + "\n"
        if self.duration is not None:
            dur = "Duration:\t" + str(self.duration) + "\n"
        return description + status + date + time + dur

    def to_dict(self) -> Dict[str, Any]:
        date = None
        if self.date is not None:
            date = self.date.strftime("%d/%m/%Y")

        time = None
        if self.time is not None:
            time = self.time.strftime("%H:%M:%S")
        return {"description": self.description, "status": self.status,
                "date": date, "time": time,
                "duration": self.duration}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Objective):
            return NotImplemented
        return (
            self.description == other.description
            and round(self.status, 2) == round(other.status, 2)
            and self.date == other.date
            and self.time == other.time
            and self.duration == other.duration
        )
