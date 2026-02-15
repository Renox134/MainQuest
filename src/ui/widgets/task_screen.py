from model.task import Task
from ui.mq_resources import ListTaskItem

import datetime

from kivymd.uix.pickers import MDModalDatePicker
from kivymd.uix.screen import MDScreen

from kivy.lang import Builder
Builder.load_file("ui/widgets/task_screen.kv")


class TaskScreen(MDScreen):

    def __init__(self, task: Task, screen_id: int, *args, **kwargs):
        self.name = f"task_screen_{str(screen_id)}"
        self.task: Task = task
        super().__init__(*args, **kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        print(self.task)
        self.ids.description_field.text = self.task.description

        if self.task.notes:
            self.ids.notes_field.text = self.task.notes
        if self.task.duedate:
            self.ids.date_button_text.text = self.task.duedate.date().strftime("%d/%m")
            self.date_dialog = MDModalDatePicker(year=self.task.duedate.year,
                                                 month=self.task.duedate.month,
                                                 day=self.task.duedate.day)
        else:
            self.date_dialog = MDModalDatePicker()
        self.date_dialog.bind(on_ok=self.confirm_date_selection)
        if self.task.duration:
            if self.task.duration < 60:
                self.ids.duration_button_text.text = f"{self.task.duration} Min"
            else:
                q, r = divmod(self.task.duration, 60)
                if r != 0:
                    self.ids.duration_button_text.text = f"{q}h {r}m"
                else:
                    self.ids.duration_button_text.text = f"{q}h"
        self.ids.subtask_list.clear_widgets()
        for subtask in self.task.subtasks:
            self.ids.subtask_list.add_widget(ListTaskItem(subtask))

    def open_date_selector(self):
        self.date_dialog.pos = [
            self.center_x - self.date_dialog.width / 2,
            self.y,
        ]
        self.date_dialog.open()

    def confirm_date_selection(self, date_dialog: MDModalDatePicker):
        if self.task.duedate is None:
            self.task.duedate = datetime.datetime(date_dialog.get_date()[0].year,
                                                  date_dialog.get_date()[0].month,
                                                  date_dialog.get_date()[0].day)
        else:
            self.task.duedate = self.task.duedate.replace(date_dialog.get_date()[0].year,
                                                          date_dialog.get_date()[0].month,
                                                          date_dialog.get_date()[0].day)
        self.update_widgets()
        date_dialog.dismiss()

    def select_time(self):
        print("Select Time")

    def set_deadline(self):
        print("Set Deadline")

    def assign_priority(self):
        print("Assign priority")