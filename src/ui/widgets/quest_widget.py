from model.quest import Quest
from kivymd.uix.boxlayout import BoxLayout
from kivymd.uix.label import MDLabel


class QuestWidget:
    """
    A widget used to display a quest.
    """

    def __init__(self, quest: Quest):
        self.quest: Quest = quest
        self.container: BoxLayout = BoxLayout()

        self.__build()

    def __build(self) -> None:
        name_label = MDLabel(text=self.quest.name)
        self.container.add_widget(name_label)
