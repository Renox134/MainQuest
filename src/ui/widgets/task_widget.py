from model.task import Task
from config_reader import Config

import datetime

import asynckivy
from kivy.lang.builder import Builder

from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon, MDListItemSupportingText, MDListItemTertiaryText, MDListItemLeadingIcon

Builder.load_file("ui/widgets/task_widget.kv")


class ExpansionPanelTaskItem(MDExpansionPanel):
    def __init__(self, task: Task=Task(description=""), **kwargs):
        self.task = task
        super().__init__(**kwargs)

    def complete_quest(self):
        print("Want to complete:\n", self.task, "\nAt ", datetime.datetime.now().strftime(Config.get("time_format")))
        

class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


class LeadingPressedIconButton(ButtonBehavior, MDListItemLeadingIcon):
    pass


class TaskWidget:
    """
    A class resembling a task widget.
    """

    def __init__(self, task: Task):
        self.task = task
        self.root = ExpansionPanelTaskItem(task=self.task)

        asynckivy.start(self.update_widget())

    async def update_widget(self) -> None:
        await asynckivy.sleep(0)
        if self.task.notes != "":
            self.root.ids.header.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.duedate is not None:
            due_date_text = "Due: " + self.task.duedate.strftime(Config.get("time_format"))
            self.root.ids.header.add_widget(MDListItemTertiaryText(text=due_date_text))
