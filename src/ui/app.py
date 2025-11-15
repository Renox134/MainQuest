from typing import Any

from model.quest_log import QuestLog
from ui.widgets.task_widget import TaskWidget, MDExpansionPanel, TrailingPressedIconButton
from ui.widgets.quest_widget import QuestWidget

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationItem

Window.size = (350, 650)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class MainQuestApp(MDApp):
    """
    The main app.
    """

    def __init__(self, quest_log: QuestLog, **kwargs: Any):
        self.quest_log = quest_log
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_file("ui/app.kv")

    def on_start(self):
        """Populate quest widgets dynamically after layout is built."""
        quest_layout = self.root.ids.quest_layout
        # for quest in self.quest_log.quests:
        #     quest_widget = QuestWidget(quest)
        #     quest_layout.add_widget(quest_widget.root)
        for _ in range(5):
            quest_layout.add_widget(QuestWidget(self.quest_log.quests[_%2]).root)

    def on_menu_pressed(self, *args):
        self.root.ids.top_app_bar.do_layout()
        print("menu pressed")

    def on_more_pressed(self, *args):
        print("three dots pressed")

    def on_nav_switch(self, *args):
        print("Called")

    def on_calendar_pressed(self, *args):
        print("Calendar pressed")

    def on_home_pressed(self, *args):
        print("Home pressed")

    def on_trophy_pressed(self, *args):
        print("Trophy pressed")

    def tap_expansion_chevron(self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton):
        print("Panel height", panel.height)
        print("Task container height", panel.ids.task_container.height)
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not panel.is_open
            else [0, 0, 0, 0],
            d=0.2,
        ).start(panel)
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)
