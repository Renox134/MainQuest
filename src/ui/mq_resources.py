from kivy.uix.screenmanager import Screen
from kivymd.uix.navigationbar import MDNavigationItem
from kivy.properties import StringProperty

from kivy.lang import Builder


class MQ_Resource_Loader():
    @staticmethod
    def load_resources() -> None:
        Builder.load_file("ui/mq_resources.kv")


class MainAppWindow(Screen):
    pass


class ProgressWindow(Screen):
    pass


class CalendarWindow(Screen):
    pass


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()
