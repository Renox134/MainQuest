from model.task import Task
from model.quest import Quest
from config import Config
from ui.mq_resources import ListTaskItem

from datetime import datetime, time

from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.pickers import MDModalDatePicker, MDTimePickerDialVertical
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivymd.uix.divider import MDDivider

from kivy.metrics import dp
from kivy.lang import Builder
Builder.load_file("ui/widgets/task_screen.kv")


class TaskScreen(MDScreen):

    def __init__(self, task: Task, parent_quest: Quest, parent_task: Task | None,
                 add_task_func, screen_id: int, *args, **kwargs):
        self.name = f"task_screen_{str(screen_id)}"
        self.task: Task = task
        self.parent_quest = parent_quest
        self.parent_task = parent_task
        self.add_task_func = add_task_func
        self.date_dialog = None
        self.time_dialog = None
        self.__time_target = 0

        super().__init__(*args, **kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        self.ids.description_field.text = self.task.description

        if self.task.notes:
            self.ids.notes_field.text = self.task.notes

        # setup the date chooser
        if self.task.date:
            self.ids.date_button_text.text = self.task.date.strftime(Config.get("date_format"))

        # setup time choosers
        if self.task.start_time:
            self.ids.start_time_button_text.text =\
                "Start: " + self.task.start_time.strftime(Config.get("time_format"))

        if self.task.end_time:
            self.ids.end_time_button_text.text =\
                "End: " + self.task.end_time.strftime(Config.get("time_format"))

        # setup subtasks
        self.ids.subtask_list.clear_widgets()
        for subtask in self.task.subtasks:
            if subtask.completion_date is None:
                self.ids.subtask_list.add_widget(ListTaskItem(subtask,
                                                              self.parent_quest, self.task))

        self.ids.subtask_list.add_widget(MDDivider())

        self.ids.subtask_list.add_widget(MDListItem(
            MDListItemHeadlineText(text="Add subtask"),
            on_release=lambda x: self.add_task_func(self))
            )

    def open_date_selector(self):
        # create the date dialogue if necessary
        if self.date_dialog is None:
            if self.task.date is None:
                self.date_dialog = MDModalDatePicker()
            else:
                self.date_dialog = MDModalDatePicker(year=self.task.date.year,
                                                     month=self.task.date.month,
                                                     day=self.task.date.day)
            self.date_dialog.bind(on_ok=self.confirm_date_selection)
            self.date_dialog.bind(on_cancel=self.date_dialog.dismiss)
        self.date_dialog.pos = [
            self.center_x - self.date_dialog.width / 2,
            self.y,
        ]
        self.date_dialog.open()

    def _on_time_select(self) -> None:
        self.confirm_time_selection(self.__time_target)

    def open_time_selector(self, idx: int) -> None:
        if self.time_dialog is None:
            self.time_dialog = MDTimePickerDialVertical()
            self.time_dialog.bind(on_cancel=self.time_dialog.dismiss)
            self.time_dialog.bind(on_ok=lambda x: self._on_time_select())

        self.__time_target = idx
        if idx == 0:
            if self.task.start_time is not None:
                self.time_dialog.set_time(self.task.start_time)
        elif idx == 1:
            if self.task.end_time is not None:
                self.time_dialog.set_time(self.task.end_time)

        self.time_dialog.pos = [
            self.center_x - self.time_dialog.width / 2,
            self.y,
        ]
        self.time_dialog.open()

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

    def confirm_time_selection(self, idx: int) -> None:
        hour: int = int(self.time_dialog.hour)
        if self.time_dialog.am_pm == "pm":
            hour = (hour + 12) % 24 if hour > 0 else 0
        minute: int = int(self.time_dialog.minute)

        if idx == 0:
            self.task.start_time = time(hour, minute)

            # if there is no endtime yet, set it to one hour later
            if self.task.end_time is None:
                if hour < 23:
                    self.task.end_time = time(hour + 1, minute)
                else:
                    self.task.end_time = time(23, 59)
            self.update_widgets()
            self.time_dialog.dismiss()
        elif idx == 1:
            if self.task.start_time <= time(hour, minute):
                self.task.end_time = time(hour, minute)
                self.update_widgets()
                self.time_dialog.dismiss()
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

    def set_deadline(self):
        MDSnackbar(
            MDSnackbarText(text="Not implemented yet :)"),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9,
        ).open()

    def assign_priority(self):
        MDSnackbar(
            MDSnackbarText(text="Not implemented yet :)"),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.9,
        ).open()
