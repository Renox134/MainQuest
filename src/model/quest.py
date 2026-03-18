from typing import List, Dict, Any, Optional

from datetime import datetime

from model.task import Task


class Quest:
    """
    A class representing a quest.

    Attributes:
        name(str): The name of the quest.
        tasks(List[Task]): The task currently allocated to this quest.
    """
    @staticmethod
    def to_quest(data: Dict[str, Any]) -> "Quest":
        """
        Creates a Quest instance from a compatible dictionary.
        """
        # Convert tasks from dicts to Task objects
        tasks = []
        for obj_data in data.get("tasks", []):
            if isinstance(obj_data, dict):
                tasks.append(Task.to_task(obj_data))
            else:
                raise ValueError(f"Invalid task type: {type(obj_data)}")

        return Quest(
            name=data.get("name", ""),
            tasks=tasks
            )

    def __init__(self, name: str = "", tasks: List[Task] = []):
        """
        Initializes a quest.

        Parameters:
            name (str): The quest name.
        """
        self.name: str = name
        self.tasks: List[Task] = tasks

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Returns a list of all tasks (including nested ones) that are assigned to this quest.

        Returns:
            List[Task]: The list of all tasks assigned to this quest (including nested ones).
        """
        all_tasks: List[Task] = []
        for task in self.tasks:
            linear_list = Task.get_linearized_task_list(task)
            for t in linear_list:
                if include_completed or t.completion_date is None:
                    all_tasks.append(t)

        return all_tasks

    def complete_all_tasks(self, time_of_completion: datetime, overwrite: bool = False) -> None:
        for task in self.tasks:
            Task.complete_task_recursively(task, time_of_completion, overwrite)

    def get_progress_dict(self) -> Dict[datetime, int]:
        result: Dict[datetime, int] = {}
        all_tasks: List[Task] = self.get_all_tasks()

        for task in all_tasks:
            if task.completion_date is None:
                continue
            result[task.completion_date] = result.get(task.completion_date, 0) + 1

        return result

    def __str__(self) -> str:
        name = "Name: \t\t" + self.name + "\n"
        obj = "tasks:\n"
        for i, o in enumerate(self.tasks):
            obj += str(o) + "\n"
            if (i == len(self.tasks) - 1):
                obj += "\n"

        return name + obj

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name,
                "tasks": [o.to_dict() for o in self.tasks]
                }

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Quest):
            return NotImplemented
        return (
            self.name == other.name
            and [obj for obj in self.tasks] == [obj for obj in other.tasks]
        )
