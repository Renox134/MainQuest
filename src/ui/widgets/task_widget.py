from model.task import Task

import asynckivy
from kivy.lang.builder import Builder

from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDListItem, MDList
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
        self.root = MDListItem()

        asynckivy.start(self.add_widgets())

    async def add_widgets(self) -> None:
        wrapper = MDBoxLayout(theme_bg_color="Custom", md_bg_color="ff0000",
                              orientation="horizontal")
        await asynckivy.sleep(0)
        
        task_panel = ExpansionPanelTaskItem(id="ExpansionPanelTaskItem")
        task_panel.text = self.task.description
        if self.task.notes != "":
            task_panel.ids.base.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.duedate is not None:
            task_panel.ids.base.add_widget(MDListItemTertiaryText(text="Due: " + self.task.duedate.strftime("%d/%m/%Y, %H:%M")))
        wrapper.add_widget(MDIconButton(icon="checkbox-blank-circle", pos_hint={"center_x": .0, "center_y": .5}))
        wrapper.add_widget(task_panel)
        self.root.ids.leading_container.add_widget(wrapper)
        self.root.ids.leading_container.size_hint_x = 1

