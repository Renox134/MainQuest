from model.task import Task
from config_reader import Config
from ui.mq_resources import ListTaskItem

from datetime import datetime, time

from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.pickers import MDModalDatePicker, MDTimePickerDialVertical
from kivymd.uix.screen import MDScreen

from kivy.metrics import dp
from kivy.lang import Builder
Builder.load_file("ui/widgets/task_screen.kv")


class TaskScreen(MDScreen):

    def __init__(self, task: Task, screen_id: int, *args, **kwargs):
        self.name = f"task_screen_{str(screen_id)}"
        self.task: Task = task
        super().__init__(*args, **kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        self.ids.description_field.text = self.task.description

        if self.task.notes:
            self.ids.notes_field.text = self.task.notes

        # setup the date chooser
        if self.task.date:
            self.ids.date_button_text.text = self.task.date.strftime(Config.get("date_format"))
            self.date_dialog = MDModalDatePicker(year=self.task.date.year,
                                                 month=self.task.date.month,
                                                 day=self.task.date.day)
        else:
            self.date_dialog = MDModalDatePicker()
        # setup time choosers
        if self.task.start_time:
            self.ids.start_time_button_text.text =\
                "Start: " + self.task.start_time.strftime(Config.get("time_format"))
            self.start_time_dialog =\
                MDTimePickerDialVertical(hour=str(self.task.start_time.hour),
                                         minute=str(self.task.start_time.minute))
        else:
            self.start_time_dialog = MDTimePickerDialVertical()
        if self.task.end_time:
            self.ids.end_time_button_text.text =\
                "End: " + self.task.end_time.strftime(Config.get("time_format"))
            self.end_time_dialog =\
                MDTimePickerDialVertical(hour=str(self.task.end_time.hour),
                                         minute=str(self.task.end_time.minute))
        else:
            self.end_time_dialog = MDTimePickerDialVertical()

        self.date_dialog.bind(on_ok=self.confirm_date_selection)
        self.date_dialog.bind(on_cancel=self.date_dialog.dismiss)
        self.start_time_dialog.bind(on_ok=self.confirm_time_selection)
        self.start_time_dialog.bind(on_cancel=self.start_time_dialog.dismiss)
        self.end_time_dialog.bind(on_ok=self.confirm_time_selection)
        self.end_time_dialog.bind(on_cancel=self.start_time_dialog.dismiss)

        # setup subtasks
        self.ids.subtask_list.clear_widgets()
        for subtask in self.task.subtasks:
            self.ids.subtask_list.add_widget(ListTaskItem(subtask))

    def open_date_selector(self):
        self.date_dialog.pos = [
            self.center_x - self.date_dialog.width / 2,
            self.y,
        ]
        self.date_dialog.open()

    def open_time_selector(self, idx: int) -> None:
        if idx == 0:
            self.start_time_dialog.pos = [
                self.center_x - self.start_time_dialog.width / 2,
                self.y,
            ]
            self.start_time_dialog.open()
        elif idx == 1:
            self.end_time_dialog.pos = [
                self.center_x - self.end_time_dialog.width / 2,
                self.y,
            ]
            self.end_time_dialog.open()

    def confirm_date_selection(self, date_dialog: MDModalDatePicker) -> None:
        if self.task.date is None:
            self.task.date = datetime(date_dialog.get_date()[0].year,
                                      date_dialog.get_date()[0].month,
                                      date_dialog.get_date()[0].day)
        else:
            self.task.date = self.task.date.replace(date_dialog.get_date()[0].year,
                                                    date_dialog.get_date()[0].month,
                                                    date_dialog.get_date()[0].day)
        self.update_widgets()
        date_dialog.dismiss()

    def confirm_time_selection(self, time_dialog: MDTimePickerDialVertical) -> None:
        hour: int = int(time_dialog.hour)
        if time_dialog.am_pm == "pm":
            hour = (hour + 12) % 24 if hour > 0 else 0
        minute: int = int(time_dialog.minute)

        if time_dialog == self.start_time_dialog:
            self.task.start_time = time(hour, minute)

            # if there is no endtime yet, set it to one hour later
            if self.task.end_time is None:
                if hour < 23:
                    self.task.end_time = time(hour + 1, minute)
                else:
                    self.task.end_time = time(23, 59)
            self.update_widgets()
            time_dialog.dismiss()
        else:
            if self.task.start_time <= time(hour, minute):
                self.task.end_time = time(hour, minute)
                self.update_widgets()
                time_dialog.dismiss()
            else:
                MDSnackbar(
                    MDSnackbarText(
                        text="The task can't end before it began.",
                    ),
                    y=dp(24),
                    pos_hint={"center_x": 0.5},
                    size_hint_x=0.9,
                ).open()

    def update_description(self):
        self.task.description = self.ids.description_field.text

    def update_notes(self):
        self.task.notes = self.ids.notes_field.text

    def select_time(self):
        print("Select Time")

    def set_deadline(self):
        print("Set Deadline")

    def assign_priority(self):
        print("Assign priority")
