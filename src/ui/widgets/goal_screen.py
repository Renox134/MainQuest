from typing import List

from model.goal import Goal
from ui.widgets.month_heat_map import MonthHeatmap
from ui.widgets.weekly_bar_chart import WeeklyBarChart
from config_reader import Config

from datetime import datetime, timedelta, date

from kivymd.uix.screen import MDScreen

from kivy.metrics import dp
from kivy.lang import Builder
Builder.load_file("ui/widgets/goal_screen.kv")

COLS = 7        # Mon–Sun
ROWS = 5        # weeks
CELL_SIZE = dp(36)
CELL_GAP = dp(5)
GRID_W = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP
GRID_H = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP

DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


class GoalScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        self.month_heatmaps: list[MonthHeatmap] = []
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        swiper = self.ids.swiper

        # create heatmap swiper widget for the current month and the two months before
        last_month = (datetime.now().replace(day=1) - timedelta(days=1))
        two_months_ago: date = (last_month.replace(day=1) - timedelta(days=1)).date()
        last_month = last_month.date()
        last_three_month_names = [MONTHS[two_months_ago.month - 1],
                                  MONTHS[last_month.month - 1],
                                  MONTHS[datetime.now().month - 1]]
        inclusion_borders = [
            (two_months_ago.replace(day=1), two_months_ago),
            (last_month.replace(day=1), last_month),
            ((datetime.now().replace(day=1)).date(), datetime.now().date())
        ]
        for month_name, borders in zip(last_three_month_names, inclusion_borders):
            month_heatmap = MonthHeatmap({}, month_name, borders)
            self.month_heatmaps.append(month_heatmap)
            swiper.add_widget(month_heatmap)

    def update_widgets(self, goal: Goal = Goal("Test")) -> None:
        self.ids.goal_title.text = goal.name

        for heatmap in self.month_heatmaps:
            heatmap.update_heatmap(goal.get_progress(), goal.high_performance_border)

        self.ids.bar_chart_layout.clear_widgets()
        self.ids.bar_chart_layout.add_widget(WeeklyBarChart(goal.get_weekly_progress()))

    def format_dates(self, unformated_dates: List[datetime]) -> List[str]:
        result = []

        for d in unformated_dates:
            to_add = d.strftime(Config.get("date_format_goal_screen"))
            result.append(to_add)

        return result
