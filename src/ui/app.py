from typing import Any, List

from journal import Journal
from model.task import Task
from model.quest import Quest
from ui.widgets.quest_widget import QuestWidget
from ui.widgets.task_screen import TaskScreen
from ui.mq_resources import MQ_Resource_Loader

from kivy.core.window import Window
import asynckivy
from kivymd.uix.screenmanager import MDScreenManager
from kivy.lang import Builder
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomsheet import MDBottomSheetDragHandleButton
from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.menu import MDDropdownMenu

from kivymd.app import MDApp

# this needs to be removed when building
Window.size = (350, 650)


class MainQuestApp(MDApp):
    """
    The main app.
    """

    def __init__(self, journal: Journal, **kwargs: Any):
        self.journal = journal
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

        for quest in self.journal.quests:
            asynckivy.start(self.add_quest_widget(quest))

        # fix header
        self.root.ids.top_app_bar.width = self.root.ids.top_app_bar.minimum_width
        self.root.ids.top_app_bar.do_layout()

    async def add_quest_widget(self, quest: Quest) -> None:
        await asynckivy.sleep(0)
        quest_layout = self.root.ids.quest_layout
        quest_widget = QuestWidget(quest, self.open_new_task_sheet)
        quest_layout.add_widget(quest_widget.root)
        self.quest_widgets.append(quest_widget)

    def add_new_quest(self, widget) -> None:
        name = self.root.ids.description_field.text

        to_add = Quest(name, [], [])

        # add quest to backend
        self.journal.quests.append(to_add)

        # add new widget to frontend
        asynckivy.start(self.add_quest_widget(to_add))

        self.root.ids.bottom_sheet.set_state("close")

    def add_new_task(self, widget) -> None:
        description = self.root.ids.description_field.text

        to_add = Task(description)

        if isinstance(widget, TaskScreen):
            # backend
            widget.task.subtasks.append(to_add)
            # frontend
            widget.update_widgets()

        elif isinstance(widget, QuestWidget):
            # backend
            widget.quest.tasks.append(to_add)
            # frontend
            widget.update_widgets() 

        self.root.ids.bottom_sheet.set_state("close")

    def open_new_task_sheet(self, calling_widget: TaskScreen | QuestWidget) -> None:
        sheet: MDBottomSheet = self.root.ids.bottom_sheet
        self.root.ids.sheet_title.text = "Add Task"
        self.root.ids.description_field_text.text = "Description"
        field: MDTextField = self.root.ids.description_field
        field.focus = True

        sheet.set_state("open")

    def open_new_quest_sheet(self) -> None:
        sheet: MDBottomSheet = self.root.ids.bottom_sheet
        self.root.ids.sheet_title.text = "Add Quest"
        self.root.ids.description_field_text.text = "Quest Name"
        field: MDTextField = self.root.ids.description_field
        field.focus = True

        confirm_button: MDBottomSheetDragHandleButton = self.root.ids.button_sheet_confirm_button
        confirm_button.bind(on_release=self.add_new_quest)

        sheet.set_state("open")

    def dummy(self) -> None:
        print("Dummy")

    def on_menu_pressed(self, *args):
        self.root.ids.top_app_bar.do_layout()
        print("menu pressed")

    def on_more_pressed(self, *args):
        drop_down = MDDropdownMenu()
        def add_quest_press():
            drop_down.dismiss()
            self.open_new_quest_sheet()
            
        menu_items = [
            {
                "text": "Add new Quest",
                "on_release": lambda: add_quest_press(),
            }
        ]
        drop_down.caller = self.root.ids.top_app_barcontext_button
        drop_down.items = menu_items
        drop_down.open()

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

    def open_task_screen(self, task: Task, parent_quest: Quest, parent_task: Task | None) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        new_task_screen: TaskScreen = TaskScreen(task, parent_quest,
                                                 parent_task, self.open_task_screens)
        manager.add_widget(new_task_screen)
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
