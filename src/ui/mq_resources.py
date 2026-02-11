from kivy.uix.screenmanager import Screen
from kivymd.uix.navigationbar import MDNavigationItem
from kivy.properties import StringProperty

from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDModalDatePicker

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


class TaskView(MDGridLayout):

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
