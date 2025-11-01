from typing import List, Dict, Any, Optional

from model.task import Task


class Quest:
    """
    A class representing a quest.
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
            
        completed_tasks = []
        for obj_data in data.get("completed_tasks", []):
            if isinstance(obj_data, dict):
                completed_tasks.append(Task.to_task(obj_data))
            else:
                raise ValueError(f"Invalid task type: {type(obj_data)}")

        return Quest(
            name=data.get("name", ""),
            tasks=tasks,
            completed_tasks=completed_tasks
        )

    def __init__(self, name: str, tasks: List[Task] = [],
                 completed_tasks: Optional[List[Task]] = None):
        """
        Initializes a quest.

        Parameters:
            name (str): The quest name.
        """
        self.name: str = name
        self.tasks: List[Task] = tasks
        self.completed_tasks: List[Task] = completed_tasks if completed_tasks is not None else []

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
                "tasks": [o.to_dict() for o in self.tasks],
                "completed_tasks": [o.to_dict() for o in self.completed_tasks]
                }

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Quest):
            return NotImplemented
        return (
            self.name == other.name
            and [obj for obj in self.tasks] == [obj for obj in other.tasks]
            and [o for o in self.completed_tasks] == [o for o in other.completed_tasks]
        )
