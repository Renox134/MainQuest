from journal import Journal
from model.quest import Quest
from ui.widgets.quest_widget import QuestWidget
from ui.widgets.dialogs import ConfirmDialog

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import MDListItem, MDListItemHeadlineText
from kivymd.uix.screen import MDScreen

from kivy.metrics import dp
from kivy.core.window import Window
from kivy.lang import Builder
Builder.load_file("ui/widgets/edit_quest_screen.kv")


class EditQuestScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def update_widgets(self, quest: Quest, journal: Journal, parent_widget: QuestWidget) -> None:
        self.quest: Quest = quest
        self.journal = journal
        self.parent_widget = parent_widget
        self.checkboxes = []
        self.ids.quest_title.text = self.quest.name
        self.ids.name_field.text = self.quest.name

        self.ids.goal_list_layout.clear_widgets()

        self.ids.goal_list_layout.add_widget(
            MDListItem(MDListItemHeadlineText(text="Associated Goals", halign="center"))
        )

        for g in self.journal.goals:
            active_on_open = self.quest in g.associated_quests
            box = MDCheckbox(id="check", active=active_on_open,
                             pos_hint={"center_x": .5, "center_y": .5})
            self.checkboxes.append(box)
            self.ids.goal_list_layout.add_widget(
                MDListItem(MDListItemHeadlineText(text=g.name), box)
            )

    def save_and_close(self) -> None:
        self.update_name()
        self.update_associating_goals()
        MDApp.get_running_app().update_progress_screen()
        MDApp.get_running_app().close_context_screen()

    def update_name(self) -> None:
        self.quest.name = self.ids.name_field.text

    def on_more_pressed(self) -> None:
        self.drop_down = MDDropdownMenu()

        menu_items = [
            {
                "text": "Clear Tasks",
                "on_release": lambda: self.clear_tasks(),
                "text_color": "red"
            },
            {
                "text": "Abort Quest",
                "on_release": lambda: self.abort_quest(),
                "text_color": "red"
            },
            {
                "text": "Delete Quest",
                "on_release": lambda: self.delete_quest(),
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

    def clear_tasks(self) -> None:
        warning_text = """
        Are you sure you want to remove all tasks?
        They will be treated as aborted and thus will not count towards the progress of any goal.
        """
        ConfirmDialog("Clear Tasks", warning_text, lambda: confirm_func()).open()

        def confirm_func():
            self.drop_down.dismiss()
            self.quest.tasks.clear()
            MDApp.get_running_app().update_quest_widgets()

    def abort_quest(self) -> None:
        warning_text = """
        Are you sure you want to abort this quest?
        The progress made until now will be kept, but all tasks that are still uncompleted
        will be treated as aborted.
        """
        ConfirmDialog("Abort Quest", warning_text, lambda: confirm_func()).open()

        def confirm_func():
            self.drop_down.dismiss()
            MDApp.get_running_app().abort_quest(self.parent_widget)
            MDApp.get_running_app().close_context_screen()

    def delete_quest(self) -> None:

        warning_text = """
        Are you sure you want to permanently delete this quest?
        By deleting the quest, all tasks are aborted and all goals will loose the all progress that
        was previously added through this quest. In contrast,aborting the quest would keep the
        progress that was already done, while only remaning tasks are aborted. 
        """
        ConfirmDialog("Delete Quest", warning_text, lambda: confirm_func()).open()

        def confirm_func():
            self.drop_down.dismiss()
            MDApp.get_running_app().delete_quest(self.parent_widget)
            MDApp.get_running_app().close_context_screen()

    def update_associating_goals(self) -> None:
        for goal, box in zip(self.journal.goals, self.checkboxes):
            if box.active:
                if self.quest not in goal.associated_quests:
                    goal.associated_quests.append(self.quest)
            else:
                if self.quest in goal.associated_quests:
                    goal.associated_quests.remove(self.quest)
