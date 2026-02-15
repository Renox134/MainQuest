from model.task import Task
from config_reader import Config

import datetime

from kivy.uix.screenmanager import Screen
from kivymd.uix.navigationbar import MDNavigationItem
from kivy.properties import StringProperty

from kivymd.uix.textfield import MDTextField
from kivymd.uix.list import MDListItem
from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.screen import MDScreen

from kivy.lang import Builder


class MainAppWindow(Screen):
    pass


class ProgressWindow(Screen):
    pass


class CalendarWindow(Screen):
    pass


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class DateSelectorField(MDTextField):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class ListTaskItem(MDListItem):
    def __init__(self, task: Task = Task(), **kwargs):
        self.task = task
        super().__init__(**kwargs)

    def complete_task(self):
        print("Want to complete:\n", self.task, "\nAt ",
              datetime.datetime.now().strftime(Config.get("time_format")))


class TaskScreen(MDScreen):

    def __init__(self, task: Task, screen_id: int, *args, **kwargs):
        self.name = f"task_screen_{str(screen_id)}"
        self.task: Task = task
        super().__init__(*args, **kwargs)
        self.fill_widgets()

    def fill_widgets(self) -> None:
        self.ids.description_field.text = self.task.description

        if self.task.notes:
            self.ids.notes_field.text = self.task.notes
        if self.task.duedate:
            self.ids.date_button_text.text = self.task.duedate.date().strftime("%d/%m")
        if self.task.duration:
            if self.task.duration < 60:
                self.ids.duration_button_text.text = f"{self.task.duration} Min"
            else:
                q, r = divmod(self.task.duration, 60)
                if r != 0:
                    self.ids.duration_button_text.text = f"{q}h {r}m"
                else:
                    self.ids.duration_button_text.text = f"{q}h"
        for subtask in self.task.subtasks:
            self.ids.subtask_list.add_widget(ListTaskItem(subtask))

    def select_date(self):
        date_dialog = MDModalDatePicker()
        date_dialog.pos = [
            self.center_x - date_dialog.width / 2,
            self.y,
        ]
        date_dialog.open()

    def select_time(self):
        print("Select Time")

    def set_deadline(self):
        print("Set Deadline")

    def assign_priority(self):
        print("Assign priority")


class MQ_Resource_Loader():
    @staticmethod
    def load_resources() -> None:
        Builder.load_file("ui/mq_resources.kv")
