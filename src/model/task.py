from typing import Dict, Any, List
import datetime


class Task:

    @staticmethod
    def to_task(data: Dict[str, Any]) -> "Task":
        """
        Creates a Task instance from a compatible dictionary.
        """
        # Parse date
        date_str = data.get("date")
        date = None
        if date_str:
            date = datetime.datetime.strptime(date_str, "%d/%m/%Y, %H:%M:%S").date()

        return Task(data.get("description", ""),
                         date, data.get("duration", 0))

    """
    A class representing a task that is to be completed.
    """
    def __init__(self, description: str,
                 subtasks: List["Task"] = [],
                 duedate: datetime.datetime | None = None,
                 completion_date: datetime.datetime | None = None,
                 duration: int | None = None):
        """
        Initializes a task.

        Parameters:
            description (str): The desription that explaines what the task is.
            date (datetime.date): Optional var for the date on which the task takes place.
            time (datetime.time): Optional var for the time at which the task takes place.
            duration (int): Optional var for the duration (in minutes) that the task takes.
        """
        self.description: str = description
        self.subtasks: List[Task] = subtasks
        self.duedate: datetime.datetime | None = duedate
        self.completion_date: datetime.datetime = completion_date
        self.duration: int | None = duration

    def __str__(self) -> str:
        description = "\nDescription: \t\t" + self.description + "\n"
        date = ""
        time = ""
        dur = ""
        if self.duedate is not None:
            date = "Duedate: \t\t" + self.duedate.strftime("%d/%m/%Y, %H:%M:%S") + "\n"
        if self.duration is not None:
            dur = "Duration:\t" + str(self.duration) + "\n"
        return description + date + time + dur

    def to_dict(self) -> Dict[str, Any]:
        duedate = None
        if self.duedate is not None:
            duedate = self.duedate.strftime("%d/%m/%Y, %H:%M:%S")

        return {"description": self.description,
                "date": duedate,
                "duration": self.duration}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.description == other.description
            and self.duedate == other.duedate
            and self.duration == other.duration
        )
