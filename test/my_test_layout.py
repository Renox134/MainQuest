from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.swiper import MDSwiperItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel

import random

# ── layout constants ──────────────────────────────────────────────────────────
COLS      = 7        # Mon–Sun
ROWS      = 5        # weeks
CELL_SIZE = 36
CELL_GAP  = 5
RADIUS    = [5]

DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December",
]

PALETTE = [
    (0.90, 0.90, 0.90, 1),
    (0.78, 0.89, 0.55, 1),
    (0.48, 0.79, 0.44, 1),
    (0.14, 0.60, 0.23, 1),
    (0.10, 0.38, 0.15, 1),
]

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    MDSwiper:
        id: swiper
        items_spacing: dp(0)
        width: root.width
'''

# ── total pixel width of the drawn grid ──────────────────────────────────────
GRID_W = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP
GRID_H = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP


class MonthHeatmap(Widget):
    """
    Canvas-only widget. Draws COLS×ROWS rounded rectangles.
    index = col * ROWS + row  (col=weekday 0-6, row=week 0-4)
    """
    def __init__(self, data: list[int], **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.clear()
        origin_x = self.x + (self.width  - GRID_W) / 2
        origin_y = self.y + (self.height - GRID_H) / 2

        with self.canvas:
            for col in range(COLS):
                for row in range(ROWS):
                    intensity = self.data[col * ROWS + row]
                    Color(*PALETTE[intensity])
                    flipped_row = (ROWS - 1) - row
                    RoundedRectangle(
                        pos=(
                            origin_x + col * (CELL_SIZE + CELL_GAP),
                            origin_y + flipped_row * (CELL_SIZE + CELL_GAP),
                        ),
                        size=(CELL_SIZE, CELL_SIZE),
                        radius=RADIUS,
                    )


def make_random_data() -> list[int]:
    weights    = [40, 20, 18, 14, 8]
    population = [i for i, w in enumerate(weights) for _ in range(w)]
    return [random.choice(population) for _ in range(COLS * ROWS)]


def build_month_item(month_name: str) -> MDSwiperItem:
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
    r_data = make_random_data()
    print(r_data)
    heatmap = MonthHeatmap(
        data=r_data,
        size_hint=(1, 1),
    )
    outer.add_widget(heatmap)

    item.add_widget(outer)
    return item


class HeatmapApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        swiper = self.root.ids.swiper
        for month_name in MONTHS:
            swiper.add_widget(build_month_item(month_name))
        return super().on_start()


HeatmapApp().run()
