from model.task import Task
from ui.mq_resources import ListTaskItem

import datetime
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.scrollview import ScrollView
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivymd.uix.pickers import MDModalDatePicker, MDTimePickerDialVertical
from kivymd.uix.screen import MDScreen
from kivymd.uix.snackbar.snackbar import MDSnackbar, MDSnackbarText

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

        # setup the date and time choosers
        if self.task.duedate:
            self.ids.date_button_text.text = self.task.duedate.strftime("%d/%m")
            self.ids.time_button_text.text = self.task.duedate.strftime("%H:%M")
            self.date_dialog = MDModalDatePicker(year=self.task.duedate.year,
                                                 month=self.task.duedate.month,
                                                 day=self.task.duedate.day)
            self.time_dialog = MDTimePickerDialVertical(hour=str(self.task.duedate.hour),
                                                        minute=str(self.task.duedate.minute))
        else:
            self.date_dialog = MDModalDatePicker()
            self.time_dialog = MDTimePickerDialVertical()

        self.date_dialog.bind(on_ok=self.confirm_date_selection)
        self.date_dialog.bind(on_cancel=self.date_dialog.dismiss)
        self.time_dialog.bind(on_ok=self.confirm_time_selection)
        self.time_dialog.bind(on_cancel=self.time_dialog.dismiss)

        # setup duration
        if self.task.duration:
            if self.task.duration < 60:
                self.ids.duration_button_text.text = f"{self.task.duration} Min"
            else:
                q, r = divmod(self.task.duration, 60)
                if r != 0:
                    self.ids.duration_button_text.text = f"{q}h {r}m"
                else:
                    self.ids.duration_button_text.text = f"{q}h"

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

    def open_time_selector(self):
        if self.task.duedate is None:
            MDSnackbar(
                MDSnackbarText(
                    text="You must select a date first.",
                ),
                y=dp(24),
                pos_hint={"center_x": 0.5},
                size_hint_x=0.7,
            ).open()
            return
        self.time_dialog.pos = [
            self.center_x - self.time_dialog.width / 2,
            self.y,
        ]
        self.time_dialog.open()

    def open_duration_selector(self) -> None:
        layout = MDBoxLayout(
            orientation="vertical",
            adaptive_height=True
        )

        # add options to layout
        option_1 = MDListItem(
            MDListItemHeadlineText(
                id="option_1_text",
                text=f"{10} Minutes"
            ),
            on_release=lambda x: self.update_duration(10)
        )
        layout.add_widget(option_1)
        option_2 = MDListItem(
            MDListItemHeadlineText(
                text=f"{15} Minutes"
            ),
            on_release=lambda x: self.update_duration(15)
        )
        layout.add_widget(option_2)
        option_3 = MDListItem(
            MDListItemHeadlineText(
                text=f"{30} Minutes"
            ),
            on_release=lambda x: self.update_duration(30)
        )
        layout.add_widget(option_3)
        option_4 = MDListItem(
            MDListItemHeadlineText(
                text=f"{1} Hour"
            ),
            on_release=lambda x: self.update_duration(60)
        )
        layout.add_widget(option_4)
        option_5 = MDListItem(
            MDListItemHeadlineText(
                text=f"{1.5} Hours"
            ),
            on_release=lambda x: self.update_duration(90)
        )
        layout.add_widget(option_5)
        option_6 = MDListItem(
            MDListItemHeadlineText(
                text=f"Custom"
            ),
        )
        layout.add_widget(option_6)

        sv = ScrollView(size_hint_y=None, height=200)
        sv.add_widget(layout)

        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Select Duration"
            ),
            MDDialogContentContainer(
                sv
            )
        )

        self.dialog.size_hint_y = 0.6
        self.dialog.update_width()
        self.dialog.open()

    def open_custom_duration_selector(self):
        return

    def confirm_date_selection(self, date_dialog: MDModalDatePicker) -> None:
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

    def confirm_time_selection(self, time_dialog: MDTimePickerDialVertical) -> None:
        hour: int = int(time_dialog.hour)
        if time_dialog.am_pm == "pm":
            hour = (hour + 12) % 24 if hour > 0 else 0
        minute: int = int(time_dialog.minute)
        self.task.duedate = self.task.duedate.replace(hour=hour, minute=minute)
        self.update_widgets()
        time_dialog.dismiss()

    def update_description(self):
        self.task.description = self.ids.description_field.text

    def update_notes(self):
        self.task.notes = self.ids.notes_field.text

    def update_duration(self, duration: int) -> None:
        self.task.duration = duration
        self.update_widgets()
        self.dialog.dismiss()

    def select_time(self):
        print("Select Time")

    def set_deadline(self):
        print("Set Deadline")

    def assign_priority(self):
        print("Assign priority")
