from typing import Any

from model.quest_log import QuestLog
from ui.widgets.quest_widget import QuestWidget

from kivy.core.window import Window
from kivymd.uix.screen import Screen
from kivymd.app import MDApp
from kivymd.uix.gridlayout import GridLayout
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.toolbar.toolbar import MDTopAppBar, MDBottomAppBar


Window.size = (350, 650)


class MainQuestApp(MDApp):
    """
    The main app.
    """
    def __init__(self, quest_log: QuestLog, **kwargs: Any):
        self.quest_log = quest_log

        super().__init__(**kwargs)

    def build(self) -> Screen:
        screen = Screen()
        main_layout = GridLayout(cols=1, rows=3)
        app_header = self.__build_app_header()
        quest_layout = BoxLayout(orientation="vertical", spacing=5, padding=10)

        main_layout.add_widget(app_header)

        for quest in self.quest_log.quests:
            quest_widget = QuestWidget(quest)
            quest_layout.add_widget(quest_widget.container)

        main_layout.add_widget(quest_layout)
        screen.add_widget(main_layout)

        return screen

    def __build_app_header(self) -> MDTopAppBar:
        """
        Builds the top bar and header for the base app.
        """
        top_bar = MDTopAppBar(title="Main Quest")
        top_bar.right_action_items = [["dots-vertical", lambda x: print("menu pressed")]]
        top_bar.left_action_items = [["menu", lambda x: print("settings pressed")]]
        return top_bar
    
    def __build_app_bottom_bar(self) -> MDBottomAppBar:
        """
        Builds the bottom bar.
        """
        bottom_bar = MDBottomAppBar()
        bottom_bar
