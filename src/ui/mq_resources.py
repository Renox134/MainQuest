from typing import List, Dict, Any

from model.task import Task
from model.quest import Quest
from model.goal import Goal
from journal import Journal
from config_reader import Config

from datetime import datetime

from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView

from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemTertiaryText, \
    MDListItemLeadingIcon, MDListItemHeadlineText
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, \
    MDDialogContentContainer
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.divider import MDDivider


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

        def change_associated_quests():
            drop_down.dismiss()
            self.open_associated_quest_dialog()

        def finish():
            drop_down.dismiss()
            self.complete_func(self)

        def abort():
            drop_down.dismiss()
            self.abort_func(self)

        def rename():
            drop_down.dismiss()
            self.open_rename_goal_dialog()

        menu_items = [
            {
                "text": "Rename Goal",
                "on_release": lambda: rename(),
            },
            {
                "text": "Change associated quests",
                "on_release": lambda: change_associated_quests(),
            },
            {
                "text": "Complete Goal",
                "on_release": lambda: finish(),
            },
            {
                "text": "Abort Goal",
                "on_release": lambda: abort(),
            }
        ]
        drop_down.caller = self.ids.context_button
        drop_down.items = menu_items
        drop_down.position = "bottom"
        drop_down.open()

    def open_rename_goal_dialog(self) -> None:
        entry_field = MDTextField(
            MDTextFieldHintText(
                text="New Goal Name"
                )
            )
        entry_field.text = self.goal.name

        def confirm_func():
            self.goal.name = entry_field.text
            self.ids.name_text_field.text = self.goal.name
            dialog.dismiss()

        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Rename Goal"),
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

    def open_associated_quest_dialog(self) -> None:
        scroll_view = ScrollView(size_hint_y=None, height=300)
        quest_list_layout = MDBoxLayout(orientation='vertical', adaptive_height=True)
        checkboxes = []

        for q in self.journal.quests:
            active_on_open = q in self.goal.associated_quests
            box = MDCheckbox(id="check", active=active_on_open,
                             pos_hint={"center_x": .5, "center_y": .5})
            checkboxes.append(box)
            quest_list_layout.add_widget(
                MDListItem(MDListItemHeadlineText(text=q.name), box)
            )

        scroll_view.add_widget(quest_list_layout)

        def confirm_func():
            new_associated_quests: List[Quest] = []
            for q, box in zip(self.journal.quests, checkboxes):
                if box.active:
                    new_associated_quests.append(q)

            self.goal.associated_quests = new_associated_quests
            dialog.dismiss()

        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Select related quests"),
            MDDialogContentContainer(
                MDDivider(),
                scroll_view,
                MDDivider(),
                orientation="vertical"
            ),
            MDDialogButtonContainer(
                Widget(),
                close_button,
                confirm_button,
                spacing="4dp"
            ),
            size_hint_y=0.75,
            pos_hint={"center_x": .5, "center_y": .5}
        )
        close_button.on_release = lambda: dialog.dismiss()

        dialog.open()


class ProgressWindow(MDScreen):

    def __init__(self, journal: Journal, *args, **kwargs):
        self.journal = journal
        super().__init__(*args, **kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        goal_list = self.ids.goal_list
        # clear old widgets if there are any
        goal_list.clear_widgets()
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

    def finish_goal(self, goal_widget: ListGoalItem) -> None:
        self.journal.finish_goal(goal_widget.goal, True)
        self.update_widgets()

    def abort_goal(self, goal_widget: ListGoalItem) -> None:
        self.journal.finish_goal(goal_widget.goal, False)
        self.update_widgets()
