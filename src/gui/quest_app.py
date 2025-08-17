from typing import List
from kivy.app import App
from kivy.lang import Builder

from model.quest import Quest
from model.quest_log import QuestLog
from gui.components.quest_list_item import QuestListItem  # noqa
from gui.components.quest_list_view import QuestListView
from gui.components.circular_progress import CircularProgress
from gui.screens.quest_screen import QuestScreen


class QuestApp(App):
    def __init__(self, quest_log: QuestLog, **kwargs):
        super().__init__(**kwargs)
        self.quest_log: QuestLog = quest_log

    def build(self):
        Builder.load_file("src/gui/quest_list.kv")

        quests: List[Quest] = self.quest_log.get_quests()

        root = QuestScreen()
        quest_list = root.ids.quest_list
        quest_list.add_widget(QuestListView(quests))
        return root
