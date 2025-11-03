from model.quest_log import QuestLog
from ui.widgets.quest_widget import QuestWidget

from kivy.core.window import Window
from kivymd.app import MDApp
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import BoxLayout


Window.size = (300, 600)


class MainQuestApp(MDApp):
    """
    The main app.
    """
    def __init__(self, quest_log: QuestLog, **kwargs):
        self.quest_log = quest_log

        super().__init__(**kwargs)

    def build(self):
        main_layout = GridLayout(cols=1, rows=3)
        quest_layout = BoxLayout(orientation="vertical", spacing=5, padding=10)

        for quest in self.quest_log.quests:
            print("Running for quest: ", quest.name)
            quest_widget = QuestWidget(quest)
            quest_layout.add_widget(quest_widget.container)

        main_layout.add_widget(quest_layout)

        return main_layout
