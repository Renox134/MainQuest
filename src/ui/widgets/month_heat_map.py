from config_reader import Config

from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex

from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.swiper import MDSwiperItem

# layout constants
COLS = 7
ROWS = 5
CELL_SIZE = dp(36)
CELL_GAP = dp(5)
RADIUS = [dp(5)]

PALETTE = [
    Config.get("month_heatmap_empty"),
    Config.get("month_heatmap_low"),
    Config.get("month_heatmap_medium"),
    Config.get("month_heatmap_high"),
]

# ── total pixel width of the drawn grid ──────────────────────────────────────
GRID_W = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP
GRID_H = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP
DAY_LABELS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


class MonthHeatmap(MDSwiperItem):
    def __init__(self, data: list[int], month_name: str, **kwargs):
        super().__init__(**kwargs)
        """
        Item Layout:

            MDSwiperItem
            └── MDBoxLayout  (vertical, tight)
                ├── MDLabel              ← month name
                ├── MDGridLayout cols=7  ← weekday header, one label per cell
                └── MonthHeatmap         ← canvas grid, expands to fill rest
        """
        outer = MDBoxLayout(
            orientation="vertical",
            padding=[0, 12, 0, 12],
            spacing=2,                  # small gap between title / header / grid
        )

        # month title
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
        self.heatmap = Heatmap(
            data=data,
            size_hint=(1, 1),
        )
        outer.add_widget(self.heatmap)

        self.add_widget(outer)


class Heatmap(Widget):
    """
    Canvas-only widget. Draws COLS x ROWS rounded rectangles.
    index = row * COLS + col  (col=weekday 0-6, row=week 0-4)
    """
    def __init__(self, data: list[int], **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.bind(pos=self._redraw, size=self._redraw)

    def _redraw(self, *_):
        self.canvas.clear()
        origin_x = self.x + (self.width - GRID_W) / 2
        origin_y = self.y + (self.height - GRID_H) / 2

        with self.canvas:
            count = 0
            # one column for each weekday
            for row in range(ROWS):
                for col in range(COLS):
                    if count == len(self.data):
                        break
                    intensity = self.data[count]
                    Color(*get_color_from_hex(PALETTE[intensity]))
                    flipped_row = (ROWS - 1) - row
                    RoundedRectangle(
                        pos=(
                            origin_x + col * (CELL_SIZE + CELL_GAP),
                            origin_y + flipped_row * (CELL_SIZE + CELL_GAP),
                        ),
                        size=(CELL_SIZE, CELL_SIZE),
                        radius=RADIUS,
                    )
                    count += 1
