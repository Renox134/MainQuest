from model.task import Task

from kivy.lang.builder import Builder
from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemTrailingIcon, MDListItemSupportingText, MDListItemTertiaryText
from kivy.properties import StringProperty

Builder.load_file("ui/widgets/task_widget.kv")


class ExpansionPanelTaskItem(MDExpansionPanel):
    text = StringProperty()


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


class TaskWidget:
    """
    A class resembling a task widget.
    """

    def __init__(self, task: Task):
        self.task = task
        self.root = ExpansionPanelTaskItem()
        if self.task.notes != "":
            self.root.ids.base.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.duedate is not None:
            self.root.ids.base.add_widget(MDListItemTertiaryText(text="Due: " + self.task.duedate.strftime("%d/%m/%Y, %H:%M")))
