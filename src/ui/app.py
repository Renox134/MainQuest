from typing import Any, List

from journal import Journal
from model.task import Task
from ui.widgets.quest_widget import QuestWidget
from ui.widgets.task_screen import TaskScreen
from ui.mq_resources import MQ_Resource_Loader

from kivy.core.window import Window
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
import asynckivy

from kivymd.app import MDApp

Window.size = (350, 650)


class MainQuestApp(MDApp):
    """
    The main app.
    """

    def __init__(self, controller: Journal, **kwargs: Any):
        self.controller = controller
        self.quest_widgets: List[QuestWidget] = []
        self.open_task_screens: int = 0
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
            for quest in self.controller.quests:
                await asynckivy.sleep(0)
                quest_widget = QuestWidget(quest)
                quest_layout.add_widget(quest_widget.root)
                self.quest_widgets.append(quest_widget)
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

    def open_task_screen(self, task: Task) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        manager.add_widget(TaskScreen(task, self.open_task_screens))
        manager.transition.direction = "left"
        manager.current = f"task_screen_{str(self.open_task_screens)}"
        self.open_task_screens += 1

    def close_task_screen(self, task_screen: TaskScreen) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        manager.transition.direction = "right"
        self.open_task_screens -= 1
        # if there is no other open task screen , go back to the main page and update quest widgets
        if self.open_task_screens == 0:
            manager.current = "main_app_screen"
            for quest_widget in self.quest_widgets:
                quest_widget.update_widgets()
        # if there is another task screen that was opened, go back to that
        else:
            manager.current = f"task_screen_{str(self.open_task_screens - 1)}"
            manager.current_screen.update_widgets()
        manager.remove_widget(task_screen)

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
