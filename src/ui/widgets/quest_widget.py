from model.quest import Quest

from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivy.properties import StringProperty



Builder.load_file("ui/widgets/quest_widget.kv")


class ExpansionPanelQuestItem(MDExpansionPanel):
    text = StringProperty()


class QuestWidget:
    """
    A widget used to display a quest.
    """

    def __init__(self, quest: Quest):
        self.quest = quest
        self.root = ExpansionPanelQuestItem()
        self.root.text = quest.name

        task_container = self.root.ids.task_container
        for task in quest.tasks:
            task_container.add_widget(MDLabel(
                text=task.description,
                adaptive_height=True,
                padding_x=dp(16),
                padding_y=dp(12)
            ))
