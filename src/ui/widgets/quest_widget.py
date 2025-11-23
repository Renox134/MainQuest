from model.quest import Quest
from ui.widgets.task_widget import TaskWidget

import asynckivy
from kivy.lang.builder import Builder
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
        asynckivy.start(self.add_widgets())

    async def add_widgets(self) -> None:
        self.root.text = self.quest.name
        task_list = self.root.ids.task_list

        for task in self.quest.tasks:
            await asynckivy.sleep(0)
            task_widget = TaskWidget(task)
            task_list.add_widget(task_widget.root)
