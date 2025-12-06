from typing import Any

from model.quest_log import QuestLog
from model.task import Task
from ui.widgets.quest_widget import QuestWidget
from ui.mq_resources import MQ_Resource_Loader, TaskBottomSheet

from kivy.core.window import Window
from kivy.lang import Builder
import asynckivy

from kivymd.app import MDApp

Window.size = (350, 650)


class MainQuestApp(MDApp):
    """
    The main app.
    """

    def __init__(self, quest_log: QuestLog, **kwargs: Any):
        self.quest_log = quest_log
        MQ_Resource_Loader().load_resources()
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_file("ui/app.kv")

    def on_start(self):
        """Populate quest widgets dynamically after layout is built."""
        quest_layout = self.root.ids.quest_layout

        async def add_quests():
            for quest in self.quest_log.quests:
                await asynckivy.sleep(0)
                quest_widget = QuestWidget(quest, self.root)
                quest_layout.add_widget(quest_widget.root)
        asynckivy.start(add_quests())

        # fix header
        self.root.ids.top_app_bar.width = self.root.ids.top_app_bar.minimum_width
        self.root.ids.top_app_bar.do_layout()

    def on_menu_pressed(self, *args):
        self.root.ids.top_app_bar.do_layout()
        print("menu pressed")

    def on_more_pressed(self, *args):
        print("three dots pressed")

    def on_nav_switch(self, *args):
        print("Nav switch")

    def on_calendar_pressed(self, *args):
        manager = self.root.ids.screen_manager
        manager.transition.direction = "left"
        self.root.ids.screen_manager.current = "calendar_window"

    def on_home_pressed(self, *args):
        manager = self.root.ids.screen_manager
        direction = ""
        match self.root.ids.screen_manager.current:
            case "progress_window":
                direction = "left"
            case "calendar_window":
                direction = "right"
            case _:
                direction = "up"
        manager.transition.direction = direction
        self.root.ids.screen_manager.current = "main_window"

    def on_trophy_pressed(self, *args):
        manager = self.root.ids.screen_manager
        manager.transition.direction = "right"
        self.root.ids.screen_manager.current = "progress_window"

    def open_task_context(self, task: Task) -> None:
        print("Test")

    def show_date_picker(self, focus):
        from kivymd.uix.pickers import MDDockedDatePicker
        from kivy.metrics import dp
        if not focus:
            return

        date_dialog = MDDockedDatePicker()
        date_dialog.pos = [
            self.center_x - date_dialog.width / 2,
            self.y - (date_dialog.height - dp(320)),
        ]
        date_dialog.open()