import pytest
import json

from model.goal import Goal
from model.quest import Quest


class TestGoal:

    def test_progress_dict_formatting(self, request: pytest.FixtureRequest):
        input_dict = request.getfixturevalue("unformated_progress_dict")
        expected = request.getfixturevalue("formated_progress_dict")
        daily_border = request.getfixturevalue("daily_border")
        lower_bound = request.getfixturevalue("lower_bound")

        assert expected == Goal.format_progress_dict(
            input_dict,
            daily_border,
            lower_bound
        )

    def test_move_quest_to_progress(self, request: pytest.FixtureRequest):
        q: Quest = request.getfixturevalue("quest_3")
        daily_border = request.getfixturevalue("daily_border")
        lower_bound = request.getfixturevalue("lower_bound")
        current = request.getfixturevalue("formated_progress_dict")
        expected = request.getfixturevalue("fused_progress_dict")

        test_goal = Goal("", [q], current, {}, lower_bound, daily_border)

        test_goal.move_quest_to_progress(q)

        assert test_goal.progress_dict == expected
