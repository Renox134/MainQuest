from model.task import Task
from model.quest import Quest
from config_reader import Config

from datetime import datetime

import matplotlib.pyplot as plt

from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.animation import Animation
from kivy.lang import Builder
from kivy_garden.matplotlib import FigureCanvasKivyAgg

from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.list import MDListItem, MDListItemSupportingText, MDListItemTertiaryText, \
    MDListItemLeadingIcon
from kivymd.uix.screen import MDScreen


class MainAppWindow(MDScreen):
    pass


class ProgressWindow(MDScreen):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
        plt.xlabel("X Axis")
        plt.ylabel("Y Axis")
        plt.title("Sample Plot")

        # Add the figure to Kivy layout
        self.add_widget(FigureCanvasKivyAgg(plt.gcf()))


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
        date_format = Config.get("date_format")
        time_format = Config.get("time_format")
        if self.task.notes != "":
            self.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.date is not None:
            due_date_text = "Due: " + self.task.date.strftime(date_format)
        if self.task.start_time is not None:
            due_date_text += f", {self.task.start_time.strftime(time_format)}"
            self.add_widget(MDListItemTertiaryText(text=due_date_text))

    def complete_task(self):
        Task.complete_task_recursively(self.task, datetime.now(), False)
        self.ids.confirm_icon.icon = "checkbox-marked-circle"
        animate_removal(self)


class MQ_Resource_Loader():
    @staticmethod
    def load_resources() -> None:
        Builder.load_file("ui/mq_resources.kv")


def animate_removal(to_remove) -> None:
    to_remove.disabled = True

    check_anim = Animation(d=0.08)
    slide_anim = Animation(opacity=0, x=to_remove.x + 80, d=0.25, t="out_quad")
    anim = check_anim + slide_anim

    def remove_item(*args):
        if to_remove.parent:
            to_remove.parent.remove_widget(to_remove)

    anim.bind(on_complete=remove_item)
    anim.start(to_remove)
