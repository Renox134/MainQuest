from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.properties import StringProperty, NumericProperty
from kivy.lang import Builder

from typing import List

from model.quest_log import QuestLog
from model.quest import Quest
from model.objective import Objective


# A single quest row in the list
class QuestListItem(BoxLayout):
    name = StringProperty("")
    status = NumericProperty(0.0)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            print(f"Clicked quest: {self.name}, Status: {self.status}")
            return True
        return super().on_touch_down(touch)


# The scrollable quest list
class QuestListView(RecycleView):
    def __init__(self, quests, **kwargs):
        super().__init__(**kwargs)
        self.data = [
            {"name": q.name, "status": q.status} for q in quests
        ]


# Root layout for the app
class QuestScreen(BoxLayout):
    pass


class QuestApp(App):
    def __init__(self, quest_log: QuestLog, **kwargs):
        super().__init__(**kwargs)
        self.quest_log: QuestLog = quest_log

    def build(self):
        Builder.load_file("src/gui/questlist.kv")

        quests: List[Quest] = self.quest_log.get_quests()

        root = QuestScreen()
        quest_list = root.ids.quest_list
        quest_list.add_widget(QuestListView(quests))
        return root
