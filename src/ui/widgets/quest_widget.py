from model.quest import Quest
from ui.widgets.task_widget import TaskWidget, TrailingPressedIconButton

import asynckivy
from kivy.lang.builder import Builder
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivy.metrics import dp
from kivy.animation import Animation


Builder.load_file("ui/widgets/quest_widget.kv")


class ExpansionPanelQuestItem(MDExpansionPanel):
    def __init__(self, quest: Quest = Quest("", []), **kwargs):
        self.quest = quest
        super().__init__(**kwargs)

    def open_quest_context(self) -> None:
        print(f"Open quest context for: {self.quest.name}")

    def tap_expansion_chevron(self, chevron: TrailingPressedIconButton):
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not self.is_open
            else [0, 0, 0, 0],
            d=0.25,
        ).start(self)
        if not self.is_open:
            self.bind(on_open=self._after_panel_open)
            self.open()
        else:
            self.close()
        self.set_chevron_down(
            chevron
        ) if not self.is_open else self.set_chevron_up(chevron)

    def _after_panel_open(self, panel):
        panel.unbind(on_open=self._after_panel_open)
        panel_content = panel.ids.expansion_content
        panel_content.height = panel_content.minimum_height
        panel_content.do_layout()


class QuestWidget:
    """
    A widget used to display a quest.
    """

    def __init__(self, quest: Quest):
        self.quest = quest
        self.root = ExpansionPanelQuestItem(quest)
        asynckivy.start(self.add_widgets())

    async def add_widgets(self) -> None:
        self.root.text = self.quest.name
        task_list = self.root.ids.task_list

        for task in self.quest.tasks:
            await asynckivy.sleep(0)
            task_widget = TaskWidget(task)
            task_list.add_widget(task_widget.root)
