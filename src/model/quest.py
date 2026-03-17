from typing import List, Dict, Any, Optional

from datetime import datetime

from model.task import Task


class Quest:
    """
    A class representing a quest.

    Attributes:
        name(str): The name of the quest.
        tasks(List[Task]): The task currently allocated to this quest.
        completed_tasks(List[Task]): All tasks that were completed as
            part of the quest.
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

    def __init__(self, name: str = "", tasks: List[Task] = [],
                 completed_tasks: Optional[List[Task]] = None):
        """
        Initializes a quest.

        Parameters:
            name (str): The quest name.
        """
        self.name: str = name
        self.tasks: List[Task] = tasks
        self.completed_tasks: List[Task] = completed_tasks if completed_tasks is not None else []

    def add_task(self, task: Task) -> None:
        """
        Adds the given task to the task list of this quest.

        Args:
            task (Task): The task to add to the task list.
        """
        self.tasks.append(task)

    def remove_task(self, task: Task) -> Task | None:
        """
        Removes the given task from the task list of this quest.

        Args:
            task (Task): The task to remove.

        Returns:
            Task | None: The task that was removed or none if it wasn't found.
        """
        if task in self.tasks:
            idx = self.tasks.index(task)
            return self.tasks.pop(idx)
        else:
            return None

    def get_all_tasks(self, include_completed: bool = True) -> List[Task]:
        """Returns a list of all tasks (including nested ones) that are assigned to this quest.

        Returns:
            List[Task]: The list of all tasks assigned to this quest (including nested ones).
        """
        all_tasks: List[Task] = []
        self.__collect_tasks_recursively(all_tasks, None, include_completed)

        return all_tasks

    def __collect_tasks_recursively(self, task_list: List[Task], current: Task | None,
                                    include_completed: bool = False) -> None:
        if current is None:
            for task in self.tasks:
                self.__collect_tasks_recursively(task_list, task)
            if include_completed:
                for completed_task in self.completed_tasks:
                    self.__collect_tasks_recursively(task_list, completed_task)
        else:
            task_list.append(current)
            for subtask in current.subtasks:
                self.__collect_tasks_recursively(task_list, subtask)
        return

    def complete_all_tasks(self, time_of_completion: datetime) -> None:
        for i in range(len(self.tasks) - 1, -1, -1):
            self.complete_task_and_subtasks(time_of_completion, self.tasks[i])

    def complete_task_and_subtasks(self, time_of_completion: datetime,
                                   to_complete: Task,
                                   parent: Task | None = None) -> None:
        # set completion times
        to_complete.completion_date = time_of_completion
        for i in range(len(to_complete.subtasks) - 1, -1, -1):
            self.complete_task_and_subtasks(time_of_completion,
                                            to_complete.subtasks[i],
                                            to_complete)
        if parent is None:
            self.tasks.remove(to_complete)
        else:
            parent.subtasks.remove(to_complete)
        self.completed_tasks.append(to_complete)

    def get_progress_dict(self) -> Dict[datetime, int]:
        result: Dict[datetime, int] = {}
        all_tasks: List[Task] = self.get_all_tasks()

        for task in all_tasks:
            if task.completion_date is None:
                continue
            result[task.completion_date] = result.get(task.completion_date, 0) + 1

        return result

    def update_completed_tasks(self) -> None:
        """
        Updates which tasks are completed and which aren't.
        """
        uncompleted_in_complete: List[Task] =\
            [t for t in self.completed_tasks if t.completion_date is None]

        completed_in_normal: List[Task] = []
        for t in self.tasks:
            if t.completion_date is not None:
                if t.completion_date <= datetime.now():
                    completed_in_normal.append(t)

        self.tasks = [t for t in self.tasks if t.completion_date is None]
        self.tasks.extend(uncompleted_in_complete)

        self.completed_tasks = [t for t in self.completed_tasks if t.completion_date is not None]
        self.completed_tasks.extend(completed_in_normal)

        # ensure the completed task list is still sorted correctly
        self.__sort_completed_tasks_by_completion_date()

    def __sort_completed_tasks_by_completion_date(self) -> None:
        """
        Sorts the completed task list, such that it is ascendingly by date of completion.
        """
        self.completed_tasks.sort(key=lambda x:
                                  x.completion_date if x.completion_date is not None
                                  else datetime.now())

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
