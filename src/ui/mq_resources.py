from kivy.uix.screenmanager import Screen
from kivymd.uix.navigationbar import MDNavigationItem
from kivy.properties import StringProperty
from model.task import Task

from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.textfield import  MDTextField
from kivymd.uix.pickers import MDDockedDatePicker, MDModalInputDatePicker, MDModalDatePicker
from kivy.metrics import dp

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
    pass

class TaskBottomSheet(MDBottomSheet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bind(on_close=self.remove_widget_when_closed)

    def remove_widget_when_closed(self, widget):
        """Removes the widget when closed, such that it doesn't stay around.

        Args:
            widget (_type_): The task view widget to remove.
        """
        widget.parent.remove_widget(widget)

    def show_date_picker(self, focus):
        if not focus:
            return

        date_dialog = MDDockedDatePicker()
        date_dialog.pos = [
            self.center_x - date_dialog.width / 2,
            self.y,
        ]
        date_dialog.open()


class MQ_Resource_Loader():
    @staticmethod
    def load_resources() -> None:
        Builder.load_file("ui/mq_resources.kv")