from typing import Dict

from config import Config

from datetime import date

from kivy.uix.widget import Widget
from kivy.graphics import Color, Line, Rectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex


# ── layout constants ──────────────────────────────────────────────────────────
BAR_GAP = dp(3)
AXIS_OFFSET_X = dp(40)   # space on the left for y-axis labels
AXIS_OFFSET_Y = dp(28)   # space at the bottom for x-axis labels
TICK_SIZE = dp(4)

MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


class WeeklyBarChart(Widget):
    """
    Canvas-only widget. Draws a bar chart displaying the progress of the
    goal it is associated with.

    `data` maps each of the last 52 week-start dates to an integer score.
    The dict is assumed to be ordered oldest → newest (Python 3.7+ dicts
    preserve insertion order, so just pass sorted(your_dict.items()) if
    needed).
    """

    def __init__(self, data: Dict[date, int], **kwargs):
        super().__init__(**kwargs)
        self.data = data
        self.bind(pos=self._redraw, size=self._redraw)

    # ── public ────────────────────────────────────────────────────────────────

    def update_data(self, data: Dict[date, int]) -> None:
        self.data = data
        self._redraw()

    # ── internals ─────────────────────────────────────────────────────────────

    def _redraw(self, *_) -> None:
        self.canvas.clear()

        if not self.data:
            return

        dates = list(self.data.keys())
        values = list(self.data.values())
        n = len(values)
        max_allowed_values = Config.get("goal_weekly_plot_max_weeks")
        if n > max_allowed_values:
            dates = dates[n - max_allowed_values:]
            values = values[n - max_allowed_values:]
            n = len(values)
        max_v = max(values) if max(values) > 0 else 1   # guard zero-division

        # ── drawable area ─────────────────────────────────────────────────────
        plot_x = self.x + AXIS_OFFSET_X          # left edge of bar area
        plot_y = self.y + AXIS_OFFSET_Y          # bottom edge of bar area
        plot_w = self.width - AXIS_OFFSET_X - dp(8)
        plot_h = self.height - AXIS_OFFSET_Y - dp(16)

        bar_w = (plot_w - (n - 1) * BAR_GAP) / n

        with self.canvas:
            # ── axes ──────────────────────────────────────────────────────────
            Color(0.55, 0.55, 0.55, 1)
            Line(points=[plot_x, plot_y, plot_x, plot_y + plot_h], width=dp(1))
            Line(points=[plot_x, plot_y, plot_x + plot_w, plot_y], width=dp(1))

            # ── y-axis ticks and labels ───────────────────────────────────────
            # Pick ~4 round tick values spread across 0 → max_v
            from kivy.core.text import Label as CoreLabel
            y_ticks = self._nice_ticks(max_v, n_ticks=4)
            for tick_v in y_ticks:
                ty = plot_y + (tick_v / max_v) * plot_h

                Color(0.55, 0.55, 0.55, 1)
                Line(points=[plot_x - TICK_SIZE, ty, plot_x, ty], width=dp(1))

                # subtle gridline
                Color(0.55, 0.55, 0.55, 0.18)
                Line(points=[plot_x, ty, plot_x + plot_w, ty], width=dp(0.8))

                # label
                lbl = CoreLabel(text=str(tick_v), font_size=dp(12))
                lbl.refresh()
                tex = lbl.texture
                Color(0.55, 0.55, 0.55, 1)
                Rectangle(
                    texture=tex,
                    pos=(plot_x - TICK_SIZE - tex.width - dp(2),
                         ty - tex.height / 2),
                    size=tex.size,
                )

            # ── y-axis title (rotated via a pre-rendered texture) ─────────────
            y_title_lbl = CoreLabel(text="Completed Tasks", font_size=dp(14))
            y_title_lbl.refresh()
            y_tex = y_title_lbl.texture
            # We can't rotate canvas instructions directly, so we draw the
            # texture using a PushMatrix/PopMatrix + Rotate instruction.
            from kivy.graphics.context_instructions import PushMatrix, PopMatrix, Rotate, Translate
            PushMatrix()
            cx = self.x + dp(8)
            cy = plot_y + plot_h / 2
            Translate(cx, cy)
            Rotate(angle=90)
            Color(0.55, 0.55, 0.55, 1)
            Rectangle(
                texture=y_tex,
                pos=(-y_tex.width / 2, -y_tex.height / 2),
                size=y_tex.size,
            )
            PopMatrix()

            # ── bars + x-axis labels ──────────────────────────────────────────
            prev_month = None

            for i, (d, v) in enumerate(zip(dates, values)):
                bx = plot_x + i * (bar_w + BAR_GAP)
                bh = (v / max_v) * plot_h if max_v > 0 else 0

                Color(*get_color_from_hex(Config.get("bar_chart_color", "#07771C")))
                Rectangle(pos=(bx, plot_y), size=(bar_w, bh))

                # x label only at the first bar of each new month
                if d.month != prev_month:
                    prev_month = d.month

                    Color(0.55, 0.55, 0.55, 1)
                    # tick mark
                    Line(
                        points=[bx + bar_w / 2, plot_y,
                                bx + bar_w / 2, plot_y - TICK_SIZE],
                        width=dp(1),
                    )
                    # month abbreviation
                    x_lbl = CoreLabel(
                        text=MONTH_ABBR[d.month - 1],
                        font_size=dp(9),
                    )
                    x_lbl.refresh()
                    x_tex = x_lbl.texture
                    Rectangle(
                        texture=x_tex,
                        pos=(bx + bar_w / 2 - x_tex.width / 2,
                             plot_y - TICK_SIZE - x_tex.height - dp(1)),
                        size=x_tex.size,
                    )

    @staticmethod
    def _nice_ticks(max_v: int, n_ticks: int = 4) -> list[int]:
        """
        Returns n_ticks evenly-spaced round integers between 0 and max_v
        (inclusive of max_v, exclusive of 0).
        """
        if max_v == 0:
            return [0]
        step = max(1, round(max_v / n_ticks))
        ticks = []
        v = step
        while v <= max_v:
            ticks.append(v)
            v += step
        if not ticks or ticks[-1] < max_v:
            ticks.append(max_v)
        return ticks
