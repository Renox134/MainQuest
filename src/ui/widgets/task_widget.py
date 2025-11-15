from model.task import Task

import asynckivy
from kivy.lang.builder import Builder

from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDIconButton
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivymd.uix.list import MDList
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
        self.root = MDList()
        asynckivy.start(self.add_widgets())

    async def add_widgets(self) -> None:
        await asynckivy.sleep(0)
        self.root.add_widget(
            MDIconButton(icon="checkbox-blank-circle", pos_hint={"center_x": .0, "center_y": .5})
        )
        
        task_panel = ExpansionPanelTaskItem()
        task_panel.text = self.task.description
        if self.task.notes != "":
            task_panel.ids.base.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.duedate is not None:
            task_panel.ids.base.add_widget(MDListItemTertiaryText(text="Due: " + self.task.duedate.strftime("%d/%m/%Y, %H:%M")))

        self.root.add_widget(task_panel)