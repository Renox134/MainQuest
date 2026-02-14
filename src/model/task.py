from typing import Dict, Any, List, Optional
import datetime

from config_reader import Config


class Task:
    """
    A class representing a task that is to be completed.

    Attributes:
        description(str): The description of what the task is.
        subtasks(List[Task]): The list of subtasks that are associated
            with this task.
        duedate(datetime.datetime): The time and date of when
            this task should be completed.
        completion_date(datetime.datetime): Time time and date at which
            the task was completed.
        duration(int): The duration (in minutes) how long the task is
            estimated to take.
    """

    @staticmethod
    def to_task(data: Dict[str, Any]) -> "Task":
        """
        Creates a Task instance from a compatible dictionary.
        """

        # Parse due date
        duedate_str = data.get("duedate")
        duedate = None
        if duedate_str:
            duedate = datetime.datetime.strptime(duedate_str, Config.get("time_format"))

        # Parse completion date
        completion_str = data.get("completion_date")
        completion_date = None
        if completion_str:
            completion_date = datetime.datetime.strptime(completion_str, Config.get("time_format"))

        # Parse subtasks (recursively)
        subtasks_data = data.get("subtasks", [])
        subtasks = [Task.to_task(st) for st in subtasks_data]

        return Task(
            description=data.get("description", ""),
            subtasks=subtasks,
            notes=data.get("notes", ""),
            duedate=duedate,
            completion_date=completion_date,
            duration=data.get("duration")
        )

    def __init__(self,
                 description: str = "",
                 subtasks: Optional[List["Task"]] = None,
                 notes: Optional[str] = None,
                 duedate: Optional[datetime.datetime] = None,
                 completion_date: Optional[datetime.datetime] = None,
                 duration: Optional[int] = None):
        """
        Initializes a task.
        """
        self.description = description
        self.subtasks = subtasks if subtasks is not None else []
        self.notes = notes if notes is not None else ""
        self.duedate = duedate
        self.completion_date = completion_date
        self.duration = duration

    def __str__(self) -> str:
        out = [f"Description:\t{self.description}"]

        if self.duedate:
            out.append(f"Duedate:\t{self.duedate.strftime(Config.get("time_format"))}")
        if self.completion_date:
            out.append(f"Completed:\t{self.completion_date.strftime(Config.get("time_format"))}")
        if self.duration is not None:
            out.append(f"Duration:\t{self.duration} minutes")

        if self.subtasks:
            out.append(f"Subtasks ({len(self.subtasks)}):")
            for sub in self.subtasks:
                out.append(f"  - {sub.description}")

        return "\n".join(out)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task to a dictionary (serializable form).
        """
        duedate_str = self.duedate.strftime(Config.get("time_format")) if self.duedate else None

        completion_str: None | str
        if self.completion_date is None:
            completion_str = None
        else:
            completion_str = self.completion_date.strftime(Config.get("time_format"))

        return {
            "description": self.description,
            "duedate": duedate_str,
            "completion_date": completion_str,
            "duration": self.duration,
            "subtasks": [s.to_dict() for s in self.subtasks]
        }

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.description == other.description and
            self.duedate == other.duedate and
            self.completion_date == other.completion_date and
            self.duration == other.duration and
            self.subtasks == other.subtasks
        )
