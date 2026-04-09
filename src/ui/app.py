from typing import Any, List, Dict

from config import Config
from journal import Journal
from model.task import Task
from model.quest import Quest
from model.goal import Goal
from ui.widgets.quest_widget import QuestWidget
from ui.widgets.task_screen import TaskScreen
from ui.widgets.goal_screen import GoalScreen
from ui.widgets.edit_goal_screen import EditGoalScreen
from ui.widgets.edit_quest_screen import EditQuestScreen
from ui.mq_resources import MQ_Resource_Loader, animate_removal, ProgressScreen
from ui.widgets.dialogs import ThemeSelectDialog, ColorPickerDialog

import os
import shutil
from datetime import datetime

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.utils import get_color_from_hex

import asynckivy

from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, \
    MDDialogContentContainer
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu


from kivymd.app import MDApp

# this needs to be set to False when building
PC_DEV = True  # times I accidentally build before setting to false: 9

if PC_DEV:
    Window.size = (350, 650)


class MainQuestApp(MDApp):
    """
    The main app.
    """

    def __init__(self, journal: Journal, **kwargs: Any):
        self.journal = journal
        self.quest_widgets: List[QuestWidget] = []
        self.open_task_screens: int = 0

        self.cache: Dict[str, Any] = {
            "completed_tasks": []
        }

        MQ_Resource_Loader().load_resources()
        super().__init__(**kwargs)

    def build(self):
        return Builder.load_file("ui/app.kv")

    def on_start(self):
        # populate journal
        self.data_path = self.find_resource_on_phone("main_quest.json")
        self.config_path = self.find_resource_on_phone("config.json")

        # overwrite during development to use local resources instead
        if PC_DEV:
            self.data_path = "src/main_quest.json"
            self.config_path = "src/config.json"

        Config.load_data(self.config_path)
        self.journal.import_journal(self.data_path)

        # initialize stylig
        self.theme_cls.primary_palette = Config.get("primary_palette", "Olive")
        self.theme_cls.theme_style = Config.get("theme_style", "Dark")

        # initialize quests
        for quest in self.journal.quests:
            asynckivy.start(self.add_quest_widget(quest))

        # fix header
        self.root.ids.top_app_bar.width = self.root.ids.top_app_bar.minimum_width
        self.root.ids.top_app_bar.do_layout()

        self.progress_screen = ProgressScreen(self.journal)
        self.root.ids.screen_manager.add_widget(self.progress_screen)

        # add screens
        Clock.schedule_once(lambda dt: self.add_goal_screen())
        Clock.schedule_once(lambda dt: self.add_edit_goal_screen())
        Clock.schedule_once(lambda dt: self.add_edit_quest_screen())

    def find_resource_on_phone(self, filename: str) -> str:
        data_path = os.path.join(self.user_data_dir, filename)

        # First launch (or after a fresh install): copy the bundled default in
        if not os.path.exists(data_path):
            bundled = resource_find(filename)
            if bundled:
                shutil.copy(bundled, data_path)

        return data_path

    async def add_quest_widget(self, quest: Quest) -> None:
        await asynckivy.sleep(0)
        quest_layout = self.root.ids.quest_layout
        quest_widget = QuestWidget(quest)
        quest_layout.add_widget(quest_widget)
        self.quest_widgets.append(quest_widget)

    def add_goal_screen(self) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        self.goal_screen = GoalScreen()
        manager.add_widget(self.goal_screen)

    def add_edit_goal_screen(self) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        self.edit_goal_screen = EditGoalScreen()
        manager.add_widget(self.edit_goal_screen)

    def add_edit_quest_screen(self) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        self.edit_quest_screen = EditQuestScreen()
        manager.add_widget(self.edit_quest_screen)

    def add_new_goal(self, name: str) -> None:
        to_add = Goal(name, progress_time_border=datetime.now())
        # add goal to backend
        self.journal.goals.append(to_add)
        # update frontend
        self.progress_screen.update_widgets()

    def add_new_quest(self, name: str) -> None:
        to_add = Quest(name, [])
        # add quest to backend
        self.journal.quests.append(to_add)
        # add new widget to frontend
        asynckivy.start(self.add_quest_widget(to_add))

    def add_new_task(self, description: str, parent_widget) -> None:
        to_add = Task(description)

        # either add task to quest or to subtasks
        if isinstance(parent_widget, TaskScreen):
            # backend
            parent_widget.task.subtasks.append(to_add)
        elif isinstance(parent_widget, QuestWidget):
            # backend
            parent_widget.quest.tasks.append(to_add)

        # frontend
        parent_widget.update_widgets()

    def open_new_quest_dialog(self) -> None:
        entry_field = MDTextField(
            MDTextFieldHintText(
                text="Quest Name"
                )
            )

        def confirm_func():
            self.add_new_quest(entry_field.text)
            dialog.dismiss()

        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Add New Quest"),
            MDDialogContentContainer(
                entry_field
            ),
            MDDialogButtonContainer(
                Widget(),
                close_button,
                confirm_button,
                spacing="4dp"
            ),
        )
        close_button.on_release = lambda: dialog.dismiss()
        entry_field.focus = True
        dialog.pos_hint = {"center_x": .5, "center_y": .75}
        dialog.open()

    def open_new_goal_dialog(self) -> None:
        entry_field = MDTextField(
            MDTextFieldHintText(
                text="Goal Name"
                )
            )

        def confirm_func():
            self.add_new_goal(entry_field.text)
            dialog.dismiss()

        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Add New Goal"),
            MDDialogContentContainer(
                entry_field
            ),
            MDDialogButtonContainer(
                Widget(),
                close_button,
                confirm_button,
                spacing="4dp"
            ),
        )
        close_button.on_release = lambda: dialog.dismiss()
        entry_field.focus = True
        dialog.pos_hint = {"center_x": .5, "center_y": .75}
        dialog.open()

    def open_new_task_dialog(self, calling_widget: TaskScreen | QuestWidget) -> None:
        entry_field = MDTextField(
            MDTextFieldHintText(
                text="Task Description"
                )
            )

        def confirm_func():
            self.add_new_task(entry_field.text, calling_widget)
            dialog.dismiss()

        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Add New Task"),
            MDDialogContentContainer(
                entry_field
            ),
            MDDialogButtonContainer(
                Widget(),
                close_button,
                confirm_button,
                spacing="4dp"
            )
        )
        close_button.on_release = lambda: dialog.dismiss()
        entry_field.focus = True
        dialog.pos_hint = {"center_x": .5, "center_y": .75}
        dialog.open()

    def finish_quest(self, quest_widget: QuestWidget) -> None:
        self.journal.finish_quest(quest_widget.quest)
        animate_removal(quest_widget)

    def abort_quest(self, quest_widget: QuestWidget) -> None:
        self.journal.finish_quest(quest_widget.quest, True, False)
        animate_removal(quest_widget)

    def delete_quest(self, quest_widget: QuestWidget) -> None:
        self.journal.finish_quest(quest_widget.quest, False, False)
        animate_removal(quest_widget)

    def dummy(self) -> None:
        print("Dummy")

    def on_menu_pressed(self, *args):
        self.root.ids.nav_drawer.set_state("toggle")
        self.root.ids.main_color_theme_text.text = "Main Theme: " + self.theme_cls.primary_palette

        # adjust for theme style
        style = self.theme_cls.theme_style
        self.root.ids.theme_style_text.text = "Theme Style: " + style
        self.root.ids.theme_style_switch.active = style == "Light"

    def select_main_color_theme(self):
        d = ThemeSelectDialog()
        d.open()

    def update_app_lighting_theme(self):
        state = "Light" if self.root.ids.theme_style_switch.active else "Dark"
        self.theme_cls.theme_style = state
        Config.store("theme_style", state)

    def open_color_picker(self, config_key: str):
        def rgb_to_hex(r, g, b):
            r = int(255 * r)
            g = int(255 * g)
            b = int(255 * b)
            return f'#{r:02X}{g:02X}{b:02X}'

        def confirm(color):
            Config.store(config_key, rgb_to_hex(color[0], color[1], color[2]))

        current_color = Config.get(config_key, "#ffffff")
        ColorPickerDialog(lambda x: confirm(x), get_color_from_hex(current_color)).open()

    def on_more_pressed(self, *args):
        drop_down = MDDropdownMenu()

        def add_quest_press():
            drop_down.dismiss()
            self.open_new_quest_dialog()

        def add_goal_press():
            drop_down.dismiss()
            self.open_new_goal_dialog()

        def save_press():
            drop_down.dismiss()
            self.save()

        menu_items = []

        # add menu items depending on the currently opened window
        if self.root.ids.screen_manager.current == "progress_screen":
            menu_items.append(
                {
                    "text": "Add new Goal",
                    "on_release": lambda: add_goal_press()
                }
            )
        elif self.root.ids.screen_manager.current == "main_window":
            menu_items.extend([
                {
                    "text": "Save",
                    "on_release": lambda: save_press()
                },
                {
                    "text": "Add new Quest",
                    "on_release": lambda: add_quest_press(),
                }
            ]
            )

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
            case "progress_screen":
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
        self.root.ids.screen_manager.current = "progress_screen"

    def open_task_screen(self, task: Task, parent_quest: Quest, parent_task: Task | None) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        new_task_screen: TaskScreen = TaskScreen(task, parent_quest,
                                                 parent_task,
                                                 self.open_new_task_dialog,
                                                 self.open_task_screens)
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

    def open_goal_screen(self, goal: Goal) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        manager.transition.direction = "left"
        self.goal_screen.update_widgets(goal)
        manager.current = "goal_screen"

    def close_context_screen(self) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        manager.transition.direction = "right"
        manager.current = "main_app_screen"

    def open_edit_goal_screen(self, goal: Goal) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        manager.transition.direction = "left"
        self.edit_goal_screen.update_widgets(goal, self.journal)
        manager.current = "edit_goal_screen"

    def open_edit_quest_screen(self, quest: Quest, parent: QuestWidget) -> None:
        manager: MDScreenManager = self.root.ids.outer_screen_manager
        manager.transition.direction = "left"
        self.edit_quest_screen.update_widgets(quest, self.journal, parent)
        manager.current = "edit_quest_screen"

    def add_task_to_completion_cache(self, task: Task) -> None:
        completed_tasks = self.cache.get("completed_tasks", [])
        completed_tasks.append(task)

    def undo_last_task(self) -> None:
        completed_tasks = self.cache.get("completed_tasks", [])
        task_to_undo = completed_tasks.pop(-1)
        completed_at = task_to_undo.completion_date
        to_revert = Task.get_linearized_task_list(task_to_undo)
        for t in to_revert:
            if t.completion_date == completed_at:
                t.completion_date = None

        self.update_quest_widgets()

    def remove_goal_from_journal(self, goal: Goal) -> None:
        self.journal.goals.remove(goal)

    def update_progress_screen(self) -> None:
        self.progress_screen.journal = self.journal
        self.progress_screen.update_widgets()

    def update_quest_widgets(self) -> None:
        for qw in self.quest_widgets:
            qw.update_widgets()

    def show_date_picker(self, focus):
        from kivymd.uix.pickers import MDDockedDatePicker
        if not focus:
            return

        date_dialog = MDDockedDatePicker()
        date_dialog.pos = [
            self.center_x - date_dialog.width / 2,
            self.y - (date_dialog.height - dp(320)),
        ]
        date_dialog.open()

    def save(self) -> None:
        self.journal.export_journal(self.data_path)
        Config.save(self.config_path)

    def on_stop(self):
        self.save()
        return super().on_stop()

    def on_pause(self):
        self.save()
        return super().on_pause()
