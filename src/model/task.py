from typing import Dict, Any, List, Optional
from datetime import datetime, date, time

from config_reader import Config


class Task:
    """
    A class representing a task that is to be completed.

    Attributes:
        description(str): The description of what the task is.
        notes(str): Some additional notes to the task.
        subtasks(List[Task]): The list of subtasks that are associated
            with this task.
        date(datetime): The date of when this task should be completed.
        start_time(time): The time at which the task starts.
        end_time(time): The time at which the task ends.
        completion_date(datetime): Time time and date at which
            the task was completed.
            estimated to take.
    """

    @staticmethod
    def to_task(data: Dict[str, Any]) -> "Task":
        """
        Creates a Task instance from a compatible dictionary.
        """

        # Parse date
        date_str = data.get("date")
        duedate = None
        if date_str:
            tmp = datetime.strptime(date_str, Config.get("date_format"))
            duedate = date(tmp.year, tmp.month, tmp.day)

        # parse start time
        start_time_str = data.get("start_time")
        start_time = None
        if start_time_str:
            start_time = time(datetime.strptime(start_time_str, Config.get("time_format")).hour,
                              datetime.strptime(start_time_str, Config.get("time_format")).minute)

        # parse start time
        end_time_str = data.get("end_time")
        end_time = None
        if end_time_str:
            end_time = time(datetime.strptime(end_time_str, Config.get("time_format")).hour,
                            datetime.strptime(end_time_str, Config.get("time_format")).minute)

        # Parse completion date
        completion_str = data.get("completion_date")
        completion_date = None
        if completion_str:
            completion_date = datetime.strptime(completion_str, Config.get("datetime_format"))

        # Parse subtasks (recursively)
        subtasks_data = data.get("subtasks", [])
        subtasks = [Task.to_task(st) for st in subtasks_data]

        return Task(
            description=data.get("description", ""),
            subtasks=subtasks,
            notes=data.get("notes", ""),
            date=duedate,
            start_time=start_time,
            end_time=end_time,
            completion_date=completion_date
            )
    
    @staticmethod
    def complete_task_recursively(to_complete: "Task",
                                  time_of_completion: datetime,
                                  overwrite: bool) -> None:
        # set completion datetime if it wasn't set before or if overwrite is activated
        if to_complete.completion_date is None or overwrite:
            to_complete.completion_date = time_of_completion
        for subtask in to_complete.subtasks:
            Task.complete_task_recursively(subtask, time_of_completion, overwrite)

    @staticmethod
    def get_linearized_task_list(task: "Task") -> List["Task"]:
        result = [task]
        # collect subtasks recursively
        for subtask in task.subtasks:
            result.extend(Task.get_linearized_task_list(subtask))     
        return result   

    def __init__(self,
                 description: str = "",
                 subtasks: Optional[List["Task"]] = None,
                 notes: Optional[str] = None,
                 date: Optional[date] = None,
                 start_time: Optional[time] = None,
                 end_time: Optional[time] = None,
                 completion_date: Optional[datetime] = None):
        """
        Initializes a task.
        """
        self.description = description
        self.subtasks: List[Task] = subtasks if subtasks is not None else []
        self.notes = notes if notes is not None else ""
        self.date = date
        self.start_time = start_time
        self.end_time = end_time
        self.completion_date = completion_date

    def get_number_of_subtasks(self) -> int:
        """
        States how many subtasks and sub-subtasks the task has.

        Returns:
            int: The total recursive number of subtasks, sub-subtasks and so on.
        """
        result = len(self.subtasks)
        if result > 0:
            result += sum([s.get_number_of_subtasks() for s in self.subtasks])
        return result

    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the Task to a dictionary (serializable form).
        """
        date_str = self.date.strftime(Config.get("date_format")) if self.date else None
        start_time_str =\
            self.start_time.strftime(Config.get("time_format")) if self.start_time else None
        end_time_str =\
            self.end_time.strftime(Config.get("time_format")) if self.end_time else None
        completion_str: None | str =\
            self.completion_date.strftime(Config.get("datetime_format")
                                          ) if self.completion_date else None

        return {
            "description": self.description,
            "date": date_str,
            "start_time": start_time_str,
            "end_time": end_time_str,
            "completion_date": completion_str,
            "subtasks": [s.to_dict() for s in self.subtasks]
        }

    def __str__(self) -> str:
        out = [f"Description:\t{self.description}"]
        date_format = Config.get("date_format")
        time_format = Config.get("time_format")
        datetime_format = Config.get("datetime_format")

        if self.date:
            out.append(f"Date:\t{self.date.strftime(date_format)}")
        if self.start_time:
            out.append(f"Start time: {self.start_time.strftime(time_format)}")
        if self.end_time:
            out.append(f"End time: {self.end_time.strftime(time_format)}")
        if self.completion_date:
            out.append("Completed:\t" +
                       f"{self.completion_date.strftime(datetime_format)}"
                       )
        if self.subtasks:
            out.append(f"Subtasks ({len(self.subtasks)}):")
            for sub in self.subtasks:
                out.append(f"  - {sub.description}")

        return "\n".join(out)

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Task):
            return NotImplemented
        return (
            self.description == other.description and
            self.date == other.date and
            self.start_time == other.start_time and
            self.end_time == other.end_time and
            self.completion_date == other.completion_date and
            self.subtasks == other.subtasks
        )
