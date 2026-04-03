from typing import List

from model.goal import Goal
from ui.widgets.month_heat_map import MonthHeatmap
from config_reader import Config

from datetime import datetime
from random import randint

from kivymd.uix.screen import MDScreen
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

from kivy.metrics import dp
from kivy.lang import Builder
Builder.load_file("ui/widgets/goal_screen.kv")

COLS = 7        # Mon–Sun
ROWS = 5        # weeks
CELL_SIZE = Config.get("month_heatmap_cell_size")
CELL_GAP = Config.get("month_heatmap_cell_gap")
GRID_W = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP
GRID_H = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP

DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


class GoalScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        self._heatmaps: list[MonthHeatmap] = []
        super().__init__(*args, **kwargs)

    def on_kv_post(self, base_widget):
        swiper = self.ids.swiper
        for month_name in MONTHS:
            vals = [i % 5 for i in range(31)]
            item, heatmap = self.build_month_item(month_name, vals)
            self._heatmaps.append(heatmap)
            swiper.add_widget(item)

    def update_widgets(self, goal: Goal = Goal("Test")) -> None:
        self.ids.goal_title.text = goal.name

        # progress_dict = goal.get_progress()
        # scores = list(progress_dict.values())
        for i, heatmap in enumerate(self._heatmaps):
            vals = [randint(0, 4) for _ in range(31)]
            heatmap.data = vals
            heatmap._redraw()

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
        return item, heatmap
