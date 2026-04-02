from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.swiper import MDSwiperItem

import random

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    MDSwiper:
        id: swiper
        size_hint: 1, 1
'''

# Green intensity palette: 0 = empty, 1-4 = progressively darker green
PALETTE = [
    (0.90, 0.90, 0.90, 1),   # 0 — empty (light gray)
    (0.78, 0.89, 0.55, 1),   # 1 — faint green
    (0.48, 0.79, 0.44, 1),   # 2 — medium green
    (0.14, 0.60, 0.23, 1),   # 3 — strong green
    (0.10, 0.38, 0.15, 1),   # 4 — deep green
]

MONTHS = [
    "January", "February", "March", "April",
    "May", "June", "July", "August",
    "September", "October", "November", "December",
]

COLS = 5   # weeks per month (simplified: always 5)
ROWS = 7   # days per week
CELL_SIZE = 32
CELL_GAP = 5
RADIUS = [5]  # RoundedRectangle corner radius


class MonthHeatmap(Widget):
    """
    A single widget that draws one month of activity as a 5×7 grid of
    rounded rectangles directly onto its canvas. No child widgets at all.

    `data` is a flat list of 35 integers (0–4), column-major order:
    index = col * 7 + row, where col=0 is week 1 and row=0 is Monday.
    """

    def __init__(self, data: list[int], **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.clear()

        # Total grid dimensions
        grid_w = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP
        grid_h = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP

        # Center the grid inside the widget
        origin_x = self.x + (self.width  - grid_w) / 2
        origin_y = self.y + (self.height - grid_h) / 2

        with self.canvas:
            for col in range(COLS):
                for row in range(ROWS):
                    idx = col * ROWS + row

                    intensity = self.data[idx] if idx < len(self.data) else 0
                    r, g, b, a = PALETTE[intensity]
                    Color(r, g, b, a)

                    # In Kivy, y=0 is the bottom, so we flip row order so
                    # row 0 (Monday) appears at the TOP of the grid.
                    flipped_row = (ROWS - 1) - row

                    cell_x = origin_x + col * (CELL_SIZE + CELL_GAP)
                    cell_y = origin_y + flipped_row * (CELL_SIZE + CELL_GAP)

                    RoundedRectangle(
                        pos=(cell_x, cell_y),
                        size=(CELL_SIZE, CELL_SIZE),
                        radius=RADIUS,
                    )


def make_random_data() -> list[int]:
    """35 random intensity values, weighted so 0 (empty) is most common."""
    weights = [40, 20, 18, 14, 8]   # probability of each intensity level
    population = [i for i, w in enumerate(weights) for _ in range(w)]
    return [random.choice(population) for _ in range(COLS * ROWS)]


class HeatmapApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        swiper = self.root.ids.swiper
        for month_name in MONTHS:
            month_label = MDLabel(text=month_name)
            wrapper = MDBoxLayout(orientation="vertical")
            # wrapper.add_widget(month_label)
            item = MDSwiperItem()
            heatmap = MonthHeatmap(data=make_random_data())
            wrapper.add_widget(heatmap)
            item.add_widget(wrapper)
            swiper.add_widget(item)
        return super().on_start()


HeatmapApp().run()