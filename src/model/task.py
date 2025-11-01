from typing import Dict, Any, List, Optional
import datetime


class Task:
    """
    A class representing a task that is to be completed.
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
            duedate = datetime.datetime.strptime(duedate_str, "%d/%m/%Y, %H:%M:%S")

        # Parse completion date
        completion_str = data.get("completion_date")
        completion_date = None
        if completion_str:
            completion_date = datetime.datetime.strptime(completion_str, "%d/%m/%Y, %H:%M:%S")

        # Parse subtasks (recursively)
        subtasks_data = data.get("subtasks", [])
        subtasks = [Task.to_task(st) for st in subtasks_data]

        return Task(
            description=data.get("description", ""),
            subtasks=subtasks,
            duedate=duedate,
            completion_date=completion_date,
            duration=data.get("duration")
        )

    def __init__(self,
                 description: str,
                 subtasks: Optional[List["Task"]] = None,
                 duedate: Optional[datetime.datetime] = None,
                 completion_date: Optional[datetime.datetime] = None,
                 duration: Optional[int] = None):
        """
        Initializes a task.
        """
        self.description = description
        self.subtasks = subtasks if subtasks is not None else []
        self.duedate = duedate
        self.completion_date = completion_date
        self.duration = duration

    def __str__(self) -> str:
        output = [f"Description:\t{self.description}"]

        if self.duedate:
            output.append(f"Duedate:\t{self.duedate.strftime('%d/%m/%Y, %H:%M:%S')}")
        if self.completion_date:
            output.append(f"Completed:\t{self.completion_date.strftime('%d/%m/%Y, %H:%M:%S')}")
        if self.duration is not None:
            output.append(f"Duration:\t{self.duration} minutes")

        if self.subtasks:
            output.append(f"Subtasks ({len(self.subtasks)}):")
            for sub in self.subtasks:
                output.append(f"  - {sub.description}")

        return "\n".join(output)

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task to a dictionary (serializable form).
        """
        duedate_str = self.duedate.strftime("%d/%m/%Y, %H:%M:%S") if self.duedate else None
        completion_str =\
            self.completion_date.strftime("%d/%m/%Y, %H:%M:%S") if self.completion_date else None

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
