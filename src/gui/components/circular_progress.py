from kivy.uix.widget import Widget
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp


class CircularProgress(Widget):
    progress = NumericProperty(0)  # 0–100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.update_canvas,
                  size=self.update_canvas,
                  progress=self.update_canvas)
        self.update_canvas()

    def update_canvas(self, *args):
        self.canvas.clear()
        with self.canvas:
            # Background circle (gray)
            Color(0.3, 0.3, 0.3)
            Ellipse(pos=self.pos, size=self.size)

            # Progress arc (blue)
            if self.progress > 0.0:
                Color(0, 0.6, 1)
                Ellipse(pos=self.pos, size=self.size,
                        angle_start=0,
                        angle_end=360 * (self.progress / 100.0))
