from model.task import Task
from config_reader import Config

from ui.widgets.task_view import TaskView

import datetime

import asynckivy
from kivy.lang.builder import Builder
from kivy.metrics import dp
from kivy.animation import Animation

from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.screen import MDScreen
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon, MDListItemSupportingText, \
    MDListItemTertiaryText, MDListItemLeadingIcon


Builder.load_file("ui/widgets/task_widget.kv")


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


class ExpansionPanelTaskItem(MDExpansionPanel):
    def __init__(self, task: Task = Task(description=""),
                 global_root: MDScreen | None = None, **kwargs):
        self.task = task
        self.global_root = global_root
        super().__init__(**kwargs)

    def open_task_context(self):
        print("Open Task Context Window")
        nav = self.global_root.ids.global_nav_layout
        bottom_sheet = TaskView(self.task, id="task_view")
        nav.add_widget(bottom_sheet)
        bottom_sheet.set_state("toggle")

    def complete_task(self):
        print("Want to complete:\n", self.task, "\nAt ",
              datetime.datetime.now().strftime(Config.get("time_format")))

    def tap_expansion_chevron(self, chevron: TrailingPressedIconButton):
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not self.is_open
            else [0, 0, 0, 0],
            d=0.25,
        ).start(self)
        if not self.is_open:
            self.bind(on_open=self._after_panel_open)
            self.open()
        else:
            self.close()
        self.set_chevron_down(
            chevron
        ) if not self.is_open else self.set_chevron_up(chevron)

    def _after_panel_open(self, panel):
        panel.unbind(on_open=self._after_panel_open)
        panel_content = panel.ids.expansion_content
        panel_content.height = panel_content.minimum_height
        panel_content.do_layout()


class LeadingPressedIconButton(ButtonBehavior, MDListItemLeadingIcon):
    pass


class TaskWidget:
    """
    A class resembling a task widget.
    """

    def __init__(self, task: Task, global_root: MDScreen | None = None):
        self.task = task
        self.root = ExpansionPanelTaskItem(task=self.task, global_root=global_root)
        self.global_root: MDScreen | None = global_root

        asynckivy.start(self.update_widget())

    async def update_widget(self) -> None:
        await asynckivy.sleep(0)
        if self.task.notes != "":
            self.root.ids.header.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.duedate is not None:
            due_date_text = "Due: " + self.task.duedate.strftime(Config.get("time_format"))
            self.root.ids.header.add_widget(MDListItemTertiaryText(text=due_date_text))

        for subtask in self.task.subtasks:
            subtask_widget = TaskWidget(subtask, self.global_root).root
            self.root.ids.subtask_list.add_widget(subtask_widget)
