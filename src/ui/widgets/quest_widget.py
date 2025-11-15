from model.quest import Quest
from ui.widgets.task_widget import TaskWidget

from kivy.lang.builder import Builder
from kivy.clock import Clock
from kivymd.uix.label import MDLabel
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

    def add_widgets(self) -> None:
        def do_add(dt) -> None:
            task_box = self.root.ids.task_list

            for task in self.quest.tasks:
                # task_box.add_widget(TaskWidget(task).root)
                task_box.add_widget(MDLabel(
                    text=task.description,
                    adaptive_height=True,
                    padding=("14dp", "12dp")
                ))
        
        Clock.schedule_once(do_add, 0)
