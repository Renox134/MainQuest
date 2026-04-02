from typing import List, Dict, Any

from model.goal import Goal
from ui.widgets.month_heat_map import MonthHeatmap
from config_reader import Config

from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

from kivy.metrics import dp
from kivy.lang import Builder
Builder.load_file("ui/widgets/goal_screen.kv")

COLS      = 7        # Mon–Sun
ROWS      = 5        # weeks
CELL_SIZE = 36
CELL_GAP  = 5
RADIUS    = [5]
GRID_W = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP
GRID_H = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP

DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


class GoalScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_widgets(self, goal: Goal = Goal("Test")) -> None:
        # self.ids.goal_title.text = goal.name

        # progress_dict = goal.get_progress()
        # scores = list(progress_dict.values())
        swiper = self.ids.swiper
        swiper.clear_widgets()

        vals = [i % 5 for i in range(35)]
        month_progress = self.build_month_item("April", vals)
        swiper.add_widget(month_progress)


    def format_dates(self, unformated_dates: List[datetime]) -> List[str]:
        result = []

        for date in unformated_dates:
            d = date.strftime(Config.get("date_format_goal_screen"))
            result.append(d)

        return result
    
    def build_month_item(self, month_name: str, data: List[int]) -> MDSwiperItem:
        """
        Layout per swiper page:

            MDSwiperItem
            └── MDBoxLayout  (vertical, tight)
                ├── MDLabel              ← month name
                ├── MDGridLayout cols=7  ← weekday header, one label per cell
                └── MonthHeatmap         ← canvas grid, expands to fill rest
        """
        item = MDSwiperItem()

        outer = MDBoxLayout(
            orientation="vertical",
            padding=[0, 12, 0, 12],
            spacing=2,                  # small gap between title / header / grid
        )

        # ── month title ───────────────────────────────────────────────────────────
        title = MDLabel(
            text=month_name,
            halign="center",
            valign="middle",
            size_hint=(1, None),
            height=dp(32),
        )
        title.bind(size=title.setter("text_size"))
        outer.add_widget(title)

        # ── weekday header (the "first row" of the logical grid) ─────────────────
        # size_hint_x=None + fixed width pins the header to exactly GRID_W pixels
        # so each cell is CELL_SIZE wide with CELL_GAP spacing — matching the
        # canvas grid below it perfectly on the x-axis.
        # pos_hint centers it horizontally inside the outer BoxLayout.
        header = MDGridLayout(
            cols=COLS,
            col_default_width=CELL_SIZE,
            col_force_default=True,
            spacing=CELL_GAP,
            size_hint=(None, None),
            width=GRID_W,
            height=dp(20),
            pos_hint={"center_x": 0.5},
        )

        for day in DAY_LABELS:
            lbl = MDLabel(
                text=day,
                halign="center",
                valign="middle",
                font_style="Body",
            )
            lbl.bind(size=lbl.setter("text_size"))
            header.add_widget(lbl)

        outer.add_widget(header)

        # ── heatmap (the "second row", spans all 7 columns implicitly) ────────────
        # size_hint_y=1 makes it absorb all vertical space not claimed by the
        # fixed-height title and header, eliminating the y-axis gap entirely.
        heatmap = MonthHeatmap(
            data=data,
            size_hint=(1, 1),
        )
        outer.add_widget(heatmap)

        item.add_widget(outer)
        return item
