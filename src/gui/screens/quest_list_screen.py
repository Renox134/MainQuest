from kivy.uix.boxlayout import BoxLayout
from kivy.factory import Factory


# Root layout for the app
class QuestListScreen(BoxLayout):
    pass


Factory.register("QuestListScreen", cls=QuestListScreen)
