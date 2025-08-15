from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import NumericProperty
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp
from kivy.uix.label import Label


class CircularProgress(RelativeLayout):
    progress = NumericProperty(0)  # 0–100

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.label = Label(text=f"{int(self.progress)}%",
                           font_size="14sp",
                           color=(1, 1, 1, 1),
                           halign="center",
                           valign="middle")
        self.add_widget(self.label)
        self.bind(pos=self.update_canvas,
                  size=self.update_canvas,
                  progress=self.update_canvas)

    def update_canvas(self, *args):
        self.canvas.before.clean()
        with self.canvas.before:
            # Background circle (gray)
            Color(0.3, 0.3, 0.3)
            Ellipse(pos=self.pos, size=self.size)

            # Progress arc (blue)
            Color(0, 0.6, 1)
            Ellipse(pos=self.pos, size=self.size,
                    angle_start=0,
                    angle_end=360 * (self.progress / 100.0))
            
        self.label.text = f"{int(self.progress)}%"
        self.label.center = self.center
