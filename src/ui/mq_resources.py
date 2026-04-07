from typing import Dict, Any

from model.task import Task
from model.quest import Quest
from model.goal import Goal
from model.milestone import Milestone
from journal import Journal
from config_reader import Config

from datetime import datetime

from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.uix.widget import Widget
from kivy.lang import Builder
from kivy.core.window import Window
from kivy.metrics import dp

from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemTertiaryText, \
    MDListItemLeadingIcon, MDListItemHeadlineText
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.app import MDApp
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, \
    MDDialogSupportingText
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarActionButton, MDSnackbarSupportingText, \
    MDSnackbarActionButtonText, MDSnackbarButtonContainer


class MainAppWindow(MDScreen):
    pass


class CalendarWindow(MDScreen):
    pass


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class LeadingPressedIconButton(ButtonBehavior, MDListItemLeadingIcon):
    pass


class ListTaskItem(MDListItem):
    def __init__(self, task: Task, parent_quest: Quest,
                 parent_task: Task | None, **kwargs):
        self.task = task
        self.parent_quest = parent_quest
        self.parent_task = parent_task
        super().__init__(**kwargs)

        self.update_widget()

    def update_widget(self) -> None:
        date_format = Config.get("date_format")
        time_format = Config.get("time_format")
        if self.task.notes != "":
            self.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.date is not None:
            due_date_text = "Due: " + self.task.date.strftime(date_format)
        if self.task.start_time is not None:
            due_date_text += f", {self.task.start_time.strftime(time_format)}"
            self.add_widget(MDListItemTertiaryText(text=due_date_text))

    def complete_task(self):
        Task.complete_task_recursively(self.task, datetime.now(), False)
        self.ids.confirm_icon.icon = "checkbox-marked-circle"
        animate_removal(self)
        MDApp.get_running_app().add_task_to_completion_cache(self.task)
        MDSnackbar(
            MDSnackbarSupportingText(
                text=f"Completed \'{self.task.description}\'",
            ),
            MDSnackbarButtonContainer(
                MDSnackbarActionButton(
                    MDSnackbarActionButtonText(
                        text="Undo"
                    ),
                    on_release=lambda x: MDApp.get_running_app().undo_last_task()
                ),
                pos_hint={"center_y": 0.5}
            ),
            y=dp(24),
            orientation="horizontal",
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9,
        ).open()


class MQ_Resource_Loader():
    @staticmethod
    def load_resources() -> None:
        Builder.load_file("ui/mq_resources.kv")


def animate_removal(to_remove) -> None:
    to_remove.disabled = True

    check_anim = Animation(d=0.08)
    slide_anim = Animation(opacity=0, x=to_remove.x + 80, d=0.25, t="out_quad")
    anim = check_anim + slide_anim

    def remove_item(*args):
        if to_remove.parent:
            to_remove.parent.remove_widget(to_remove)

    anim.bind(on_complete=remove_item)
    anim.start(to_remove)


class ListGoalItem(MDListItem):
    def __init__(self, journal: Journal, goal: Goal, callables: Dict[str, Any], *args, **kwargs):
        self.journal = journal
        self.goal = goal
        self.complete_func = callables.get("complete_goal")
        self.abort_func = callables.get("abort_goal")
        super().__init__(*args, **kwargs)

    def open_goal_context(self) -> None:
        drop_down = MDDropdownMenu()

        def edit():
            drop_down.dismiss()
            MDApp.get_running_app().open_edit_goal_screen(self.goal)

        def finish():
            drop_down.dismiss()
            # double check via dialog
            doublecheck_line = f"Are you sure you want to set \'{self.goal.name}\' to completed?"
            close_button = MDIconButton(icon="close")
            dialog = MDDialog(
                MDDialogHeadlineText(text="Complete Goal"),
                MDDialogSupportingText(text=doublecheck_line),
                MDDialogButtonContainer(
                    Widget(),
                    MDIconButton(icon="check", on_release=lambda x: confirm()),
                    close_button
                )
            )
            close_button.on_release = lambda: dialog.dismiss()

            def confirm():
                dialog.dismiss()
                self.complete_func(self)
            dialog.open()

        menu_items = [
            {
                "text": "Edit Goal",
                "on_release": lambda: edit(),
            },
            {
                "text": "Complete Goal",
                "on_release": lambda: finish(),
            }
        ]
        drop_down.caller = self.ids.context_button
        drop_down.items = menu_items
        drop_down.position = "bottom"
        drop_down.max_width = "200dp"
        drop_down.open()

        # Clamp it so it never goes off the right edge of the screen
        menu_width = drop_down.width
        caller_x = self.ids.context_button.to_window(*self.ids.context_button.pos)[0]
        if caller_x + menu_width > Window.width:
            drop_down.x = Window.width - menu_width - dp(8)


class ListMilestoneItem(MDListItem):
    def __init__(self, milestone: Milestone, *args, **kwargs):
        self.milestone = milestone
        super().__init__(*args, **kwargs)

    def update_texts(self) -> None:
        self.ids.name_text_field.text = self.milestone.name
        self.ids.supporting_text.text = self.milestone.datetime.strftime(Config.get("date_format"))


class ProgressScreen(MDScreen):

    def __init__(self, journal: Journal, *args, **kwargs):
        self.journal = journal
        super().__init__(*args, **kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        goal_list = self.ids.goal_list
        # clear old widgets if there are any
        goal_list.clear_widgets()
        goal_list.add_widget(
            MDListItem(MDListItemHeadlineText(text="Goals", halign="center"))
        )
        for g in self.journal.goals:
            goal_list.add_widget(
                ListGoalItem(
                    self.journal,
                    g,
                    {
                        "complete_goal": self.finish_goal,
                        "abort_goal": self.abort_goal
                    }
                )
            )

        # add milestones
        milestone_list = self.ids.milestone_list
        milestone_list.clear_widgets()
        milestone_list.add_widget(
            MDListItem(MDListItemHeadlineText(text="Milestones", halign="center"))
        )
        for m in self.journal.milestones:
            to_add = ListMilestoneItem(m)
            milestone_list.add_widget(to_add)
            to_add.update_texts()

    def finish_goal(self, goal_widget: ListGoalItem) -> None:
        self.journal.finish_goal(goal_widget.goal, True)
        self.update_widgets()

    def abort_goal(self, goal_widget: ListGoalItem) -> None:
        self.journal.finish_goal(goal_widget.goal, False)
        self.update_widgets()
