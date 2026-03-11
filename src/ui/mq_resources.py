from model.task import Task
from model.quest import Quest
from config_reader import Config

from datetime import datetime

from kivymd.uix.navigationbar import MDNavigationItem
from kivy.properties import StringProperty

from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemTertiaryText, \
    MDListItemLeadingIcon
from kivymd.uix.screen import MDScreen

from kivy.animation import Animation
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
    def __init__(self, task: Task, parent_quest: Quest,
                 parent_task: Task | None, **kwargs):
        self.task = task
        self.parent_quest = parent_quest
        self.parent_task = parent_task
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
        if self.parent_task is None:
            self.parent_quest.complete_task_and_subtasks(datetime.now(), self.task)
        else:
            self.parent_quest.complete_task_and_subtasks(datetime.now(),
                                                         self.task,
                                                         self.parent_task)
        self.ids.confirm_icon.icon = "checkbox-marked-circle"
        self.animate_removal()

    def animate_removal(self) -> None:
        self.disabled = True

        anim = Animation(
            opacity=0,
            x=self.x - 80,   # slide left
            d=0.25,
            t="out_quad"
        )

        def remove_item(*args):
            if self.parent:
                self.parent.remove_widget(self)

        anim.bind(on_complete=remove_item)
        anim.start(self)


class MQ_Resource_Loader():
    @staticmethod
    def load_resources() -> None:
        Builder.load_file("ui/mq_resources.kv")
