from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty


class QuestListItem(BoxLayout):
    """
    1 quest row
    """
    name = StringProperty("")
    status = NumericProperty(0.0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(f"Clicked quest: {self.name}, Status: {self.status}")
            return True
        return super().on_touch_down(touch)
