from config_reader import Config

from kivy.uix.widget import Widget
from kivy.graphics import Color, RoundedRectangle

# layout constants
COLS = 7        # Mon–Sun
ROWS = 5        # weeks
CELL_SIZE = Config.get("month_heatmap_cell_size")
CELL_GAP = Config.get("month_heatmap_cell_gap")
RADIUS = Config.get("month_heatmap_radius")

PALETTE = [
    (0.90, 0.90, 0.90, 1),
    (0.78, 0.89, 0.55, 1),
    (0.48, 0.79, 0.44, 1),
    (0.14, 0.60, 0.23, 1),
    (0.10, 0.38, 0.15, 1),
]

# ── total pixel width of the drawn grid ──────────────────────────────────────
GRID_W = COLS * CELL_SIZE + (COLS - 1) * CELL_GAP
GRID_H = ROWS * CELL_SIZE + (ROWS - 1) * CELL_GAP


class MonthHeatmap(Widget):
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
                    count += 1
