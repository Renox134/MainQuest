from typing import Dict, Any

from model.quest import Quest
from ui.mq_resources import ListTaskItem

from kivy.lang.builder import Builder
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.uix.widget import Widget

from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.behaviors import RotateBehavior
from kivymd.uix.list import MDListItemTrailingIcon
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, \
    MDDialogContentContainer
from kivymd.uix.button import MDIconButton


Builder.load_file("ui/widgets/quest_widget.kv")


class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


class QuestWidget(MDExpansionPanel):
    def __init__(self, quest: Quest, callables: Dict[str, Any], **kwargs):
        self.quest = quest
        self.add_task_func = callables["add_task"]
        self.finish_quest_func = callables["finish_quest"]
        self.abort_quest_func = callables["abort_quest"]
        super().__init__(**kwargs)
        self.update_widgets()

    def update_widgets(self) -> None:
        self.ids.task_list.clear_widgets()
        for task in self.quest.tasks:
            if task.completion_date is None:
                self.ids.task_list.add_widget(ListTaskItem(task, self.quest, None))

    def open_quest_context(self) -> None:
        drop_down = MDDropdownMenu()

        def add_task():
            drop_down.dismiss()
            self.add_task_func(self)

        def finish():
            drop_down.dismiss()
            self.finish_quest_func(self)

        def abort():
            drop_down.dismiss()
            self.abort_quest_func(self)

        def rename():
            drop_down.dismiss()
            self.open_rename_quest_diallog()

        menu_items = [
            {
                "text": "Rename Quest",
                "on_release": lambda: rename(),
            },
            {
                "text": "Add new Task",
                "on_release": lambda: add_task(),
            },
            {
                "text": "Complete quest",
                "on_release": lambda: finish(),
            },
            {
                "text": "Abort quest",
                "on_release": lambda: abort(),
            }
        ]
        drop_down.caller = self.ids.context_button
        drop_down.items = menu_items
        drop_down.position = "center"
        drop_down.open()

    def open_rename_quest_diallog(self) -> None:
        entry_field = MDTextField(
            MDTextFieldHintText(
                text="New Quest Name"
                )
            )
        entry_field.text = self.quest.name

        def confirm_func():
            self.quest.name = entry_field.text
            self.ids.name_text_field.text = self.quest.name
            dialog.dismiss()

        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Rename Quest"),
            MDDialogContentContainer(
                entry_field
            ),
            MDDialogButtonContainer(
                Widget(),
                close_button,
                confirm_button,
                spacing="4dp"
            ),
        )
        close_button.on_release = lambda: dialog.dismiss()
        entry_field.focus = True
        dialog.pos_hint = {"center_x": .5, "center_y": .75}
        dialog.open()

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
