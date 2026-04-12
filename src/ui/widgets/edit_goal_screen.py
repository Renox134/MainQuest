from journal import Journal
from model.goal import Goal

from datetime import datetime

from kivymd.app import MDApp
from kivymd.uix.button import MDIconButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivymd.uix.screen import MDScreen
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, \
    MDDialogSupportingText

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.lang import Builder
Builder.load_file("ui/widgets/edit_goal_screen.kv")


class EditGoalScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_widgets(self, goal: Goal, journal: Journal) -> None:
        self.goal: Goal = goal
        self.journal = journal
        self.checkboxes = []
        self.ids.goal_title.text = self.goal.name
        self.ids.name_field.text = self.goal.name

        self.ids.quest_list_layout.clear_widgets()

        self.ids.quest_list_layout.add_widget(
            MDListItem(MDListItemHeadlineText(text="Associated Quests", halign="center"))
        )

        for q in self.journal.quests:
            active_on_open = q in self.goal.associated_quests
            box = MDCheckbox(id="check", active=active_on_open,
                             pos_hint={"center_x": .5, "center_y": .5})
            self.checkboxes.append(box)
            self.ids.quest_list_layout.add_widget(
                MDListItem(MDListItemHeadlineText(text=q.name), box)
            )

    def save_and_close(self) -> None:
        self.update_name()
        self.update_associated_quests()
        self.update_high_performance_border()
        MDApp.get_running_app().update_progress_screen()
        MDApp.get_running_app().close_context_screen()

    def update_name(self) -> None:
        self.goal.name = self.ids.name_field.text

    def on_more_pressed(self) -> None:
        self.drop_down = MDDropdownMenu()

        menu_items = [
            {
                "text": "Reset Progress",
                "on_release": lambda: self.reset_progress(),
                "text_color": "red"
            },
            {
                "text": "Remove Goal",
                "on_release": lambda: self.delete_goal(),
                "text_color": "red"
            }
        ]
        self.drop_down.caller = self.ids.context_button
        self.drop_down.items = menu_items
        self.drop_down.position = "bottom"
        self.drop_down.max_width = "200dp"
        self.drop_down.open()

        # Clamp it so it never goes off the right edge of the screen
        menu_width = self.drop_down.width
        caller_x = self.ids.context_button.to_window(*self.ids.context_button.pos)[0]
        if caller_x + menu_width > Window.width:
            self.drop_down.x = Window.width - menu_width - dp(8)

    def reset_progress(self) -> None:
        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Reset Progress"),
            MDDialogSupportingText(text="Are you sure you want to reset the progress?"),
            MDDialogButtonContainer(
                Widget(),
                close_button,
                confirm_button,
                spacing="4dp"
            ),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        close_button.on_release = lambda: dialog.dismiss()
        dialog.open()

        def confirm_func():
            self.drop_down.dismiss()
            dialog.dismiss()
            self.goal.progress_time_border = datetime.now().date()
            MDApp.get_running_app().close_context_screen()

    def delete_goal(self) -> None:
        confirm_button = MDIconButton(icon="check",
                                      on_release=lambda x: confirm_func())
        close_button = MDIconButton(icon="close")
        dialog = MDDialog(
            MDDialogHeadlineText(text="Delete Goal"),
            MDDialogSupportingText(text="Are you sure you want to permanently delete the goal?"),
            MDDialogButtonContainer(
                Widget(),
                close_button,
                confirm_button,
                spacing="4dp"
            ),
            pos_hint={"center_x": .5, "center_y": .5}
        )
        close_button.on_release = lambda: dialog.dismiss()
        dialog.open()

        def confirm_func():
            self.drop_down.dismiss()
            dialog.dismiss()
            MDApp.get_running_app().remove_goal_from_journal(self.goal)
            MDApp.get_running_app().update_progress_screen()
            MDApp.get_running_app().close_context_screen()

    def update_associated_quests(self) -> None:
        new_list = []
        for q, box in zip(self.journal.quests, self.checkboxes):
            if box.active:
                new_list.append(q)

        self.goal.associated_quests = new_list

    def update_high_performance_border(self) -> None:
        self.goal.high_performance_border = int(self.ids.slider.value)

    def on_enter(self):
        Window.bind(on_keyboard=self.back_click)

    def on_pre_leave(self):
        Window.unbind(on_keyboard=self.back_click)

    def back_click(self, window, key, keycode, *largs):
        if key == 27:
            # Navigate to previous screen
            self.save_and_close()
            return True
        return False
