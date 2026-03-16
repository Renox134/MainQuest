from model.quest import Quest
from ui.mq_resources import ListTaskItem

from kivy.lang.builder import Builder
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.list import MDListItemTrailingIcon
from kivymd.uix.menu import MDDropdownMenu
from kivy.metrics import dp
from kivy.animation import Animation


Builder.load_file("ui/widgets/quest_widget.kv")


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


class QuestWidget(MDExpansionPanel):
    def __init__(self, quest: Quest, add_task_func, **kwargs):
        self.quest = quest
        self.add_task_func = add_task_func
        super().__init__(**kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        self.text = self.quest.name

        self.ids.task_list.clear_widgets()
        for task in self.quest.tasks:
            self.ids.task_list.add_widget(ListTaskItem(task, self.quest, None))

    def open_quest_context(self) -> None:
        drop_down = MDDropdownMenu()

        def add_task():
            drop_down.dismiss()
            self.add_task_func(self)

        menu_items = [
            {
                "text": "Add new Task",
                "on_release": lambda: add_task(),
            },
            {
                "text": "Complete quest",
                "on_release": lambda: print("Complete quest button pressed"),
            }
        ]
        drop_down.caller = self.ids.context_button
        drop_down.items = menu_items
        drop_down.open()

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
