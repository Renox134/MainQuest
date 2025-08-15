from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, NumericProperty
from kivy.factory import Factory


class QuestListItem(BoxLayout):
    """
    1 quest row
    """
    name = StringProperty("")
    status = NumericProperty(0.0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            app = App.get_running_app()
            app.show_quest_detail(self.name)
            return True
        return super().on_touch_down(touch)



Factory.register("QuestListItem", cls=QuestListItem)
