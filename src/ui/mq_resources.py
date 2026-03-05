from model.task import Task
from config_reader import Config

from datetime import datetime

from kivymd.uix.navigationbar import MDNavigationItem
from kivy.properties import StringProperty

from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemTertiaryText, \
    MDListItemLeadingIcon
from kivymd.uix.screen import MDScreen

from kivy.lang import Builder


class MainAppWindow(MDScreen):
    pass


class ProgressWindow(MDScreen):
    pass


class CalendarWindow(MDScreen):
    pass


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class LeadingPressedIconButton(ButtonBehavior, MDListItemLeadingIcon):
    pass


class ListTaskItem(MDListItem):
    def __init__(self, task: Task = Task(), **kwargs):
        self.task = task
        super().__init__(**kwargs)

        self.update_widget()

    def update_widget(self) -> None:
        if self.task.notes != "":
            self.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.date is not None:
            due_date_text = "Due: " + self.task.date.strftime(Config.get("date_format"))
        if self.task.start_time is not None:
            due_date_text += f", {self.task.start_time.strftime(Config.get("time_format"))}"
            self.add_widget(MDListItemTertiaryText(text=due_date_text))

    def complete_task(self):
        print("Want to complete:\n", self.task, "\nAt ",
              datetime.now().strftime(Config.get("datetime_format")))


class MQ_Resource_Loader():
    @staticmethod
    def load_resources() -> None:
        Builder.load_file("ui/mq_resources.kv")
