from model.quest import Quest
from ui.widgets.task_widget import TaskWidget

from kivy.metrics import dp
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.expansionpanel import MDExpansionPanel, MDExpansionPanelContent
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

        # task_container = self.root.ids.task_container
        # task_container.add_widget(MDLabel(text="Channel information", adaptive_height=True, 
        #                                   padding_x="16dp", padding_y="12dp"))
        # task_container.height = task_container.minimum_height
        # task_box = BoxLayout(orientation="vertical")
        # for task in quest.tasks:
        #     # task_container.add_widget(TaskWidget(task).root)
        #     task_box.add_widget(MDLabel(
        #         text=task.description,
        #         adaptive_height=True,
        #         padding_x=dp(16),
        #         padding_y=dp(12)
        #     ))
        # task_container.add_widget(task_box)
