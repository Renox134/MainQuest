from model.task import Task
from ui.mq_resources import ListTaskItem
from config_reader import Config

import asynckivy
from kivy.lang.builder import Builder


from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.list import MDListItemSupportingText, MDListItemTertiaryText, \
    MDListItemLeadingIcon, MDListItem


# Builder.load_file("ui/widgets/task_widget.kv")


class LeadingPressedIconButton(ButtonBehavior, MDListItemLeadingIcon):
    pass


class TaskWidget:
    """
    A class resembling a task widget.
    """

    def __init__(self, task: Task):
        self.task = task
        self.root = ListTaskItem(task=self.task)

        asynckivy.start(self.update_widget())

    async def update_widget(self) -> None:
        await asynckivy.sleep(0)
        if self.task.notes != "":
            self.root.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.duedate is not None:
            due_date_text = "Due: " + self.task.duedate.strftime(Config.get("time_format"))
            self.root.add_widget(MDListItemTertiaryText(text=due_date_text))
