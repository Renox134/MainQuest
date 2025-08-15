from typing import List
from kivy.app import App
from kivy.lang import Builder

from model.quest import Quest
from model.quest_log import QuestLog
import gui.components
import gui.screens


class QuestApp(App):
    def __init__(self, quest_log: QuestLog, **kwargs):
        super().__init__(**kwargs)
        self.quest_log: QuestLog = quest_log

    def show_quest_detail(self, quest_name):
        quest = next((q for q in self.quest_log.get_quests() if q.name == quest_name), None)
        if quest:
            detail_screen = self.root.get_screen("quest_detail")
            detail_screen.populate(quest)
            self.root.current = "quest_detail"


    def build(self):
        Builder.load_file("src/gui/questlist.kv")

        quests: List[Quest] = self.quest_log.get_quests()

        root = gui.screens.QuestListScreen()
        quest_list = root.ids.quest_list
        quest_list.add_widget(gui.components.QuestListView(quests))
        return root
