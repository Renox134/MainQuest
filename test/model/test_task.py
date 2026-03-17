import pytest

from model.task import Task


class TestTask:

    @pytest.mark.parametrize(
            "taskname,number_of_subtasks",
            (("test_task_1", 4),
             ("test_task_2", 0),
             ("test_task_3", 0))
    )
    def test_subtask_count(self, taskname: str, number_of_subtasks: int, request: pytest.FixtureRequest):
        task: Task = request.getfixturevalue(taskname)

        assert number_of_subtasks == task.get_number_of_subtasks()
