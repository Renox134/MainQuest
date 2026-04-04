from typing import List

from model.goal import Goal
from ui.widgets.month_heat_map import MonthHeatmap, Heatmap
from config_reader import Config

from datetime import datetime
import random
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
        self._heatmaps: list[Heatmap] = []
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        swiper = self.ids.swiper
        for month_name in MONTHS:
            vals = [i % 4 for i in range(31)]
            month_heatmap = MonthHeatmap(vals, month_name)
            self._heatmaps.append(month_heatmap.heatmap)
            swiper.add_widget(month_heatmap)

    def update_widgets(self, goal: Goal = Goal("Test")) -> None:
        self.ids.goal_title.text = goal.name

        # progress_dict = goal.get_progress()
        # scores = list(progress_dict.values())
        for i, heatmap in enumerate(self._heatmaps):
            vals = self.make_random_data()
            heatmap.data = vals
            heatmap._redraw()

    def make_random_data(self) -> list[int]:
        """35 random intensity values, weighted so 0 (empty) is most common."""
        weights = [60, 40, 15, 10]   # probability of each intensity level
        population = [i for i, w in enumerate(weights) for _ in range(w)]
        return [random.choice(population) for _ in range(31)]

    def format_dates(self, unformated_dates: List[datetime]) -> List[str]:
        result = []

        for date in unformated_dates:
            d = date.strftime(Config.get("date_format_goal_screen"))
            result.append(d)

        return result
