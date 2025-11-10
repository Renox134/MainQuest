from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import MDListItemSupportingText, MDListItemTertiaryText

from src.model.task import Task

import datetime

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor
    
    BoxLayout:
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint_x: 0.7

        MDIconButton:
            id: checkbutton
            on_release: app.on_task_press()
            icon: "checkbox-blank-circle"
            pos_hint: {"center_x": .5, "center_y": .5}
    
        MDListItem:
            id: base
            pos_hint: {"center_x": .5, "center_y": .5}
            on_release: app.on_task_press()
            MDListItemHeadlineText:
                id: description
            MDListItemTrailingIcon:
                id: chevron
                icon: "chevron-left"
                pos_hint: {"center_x": .5, "center_y": .5}
'''


class TestApp(MDApp):
    def build(self):
        self.screen = MDScreen()
        self.task: Task = Task(description="Create Task Widget",
                               subtasks=[Task("Subtask 1"), Task("Subtask 2", datetime.datetime(2025, 11, 20, 12, 20, 0), duration=30)],
                               notes="Once the task widget works, I can focus on more exiting tasks.",
                               duedate=datetime.datetime(2025, 11, 20, 12, 20, 0), duration=30)
        self.root = Builder.load_string(KV)
        self.root.ids.description.text = self.task.description
        if self.task.notes != "":
            self.root.ids.base.add_widget(MDListItemSupportingText(text=self.task.notes))
        if self.task.duedate is not None:
            self.root.ids.base.add_widget(MDListItemTertiaryText(text="Due: " + self.task.duedate.strftime("%d/%m/%Y, %H:%M")))

        return self.root
    
    def on_task_press(self, *args):
        print("Pressed")
        if self.root.ids.checkbutton.icon == "checkbox-blank-circle":
            self.root.ids.checkbutton.icon = "checkbox-marked-circle"
        else:
            self.root.ids.checkbutton.icon = "checkbox-blank-circle"
    
t = TestApp()
t.run()
