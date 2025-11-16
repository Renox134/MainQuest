from kivy.lang import Builder
from kivymd.app import MDApp


from kivymd.uix.behaviors import RotateBehavior
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.list import *
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.button import MDIconButton
from kivymd.uix.expansionpanel import *
import asynckivy
from kivy.properties import StringProperty
from kivy.core.window import Window


Window.size = (350, 650)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()

class TrailingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
):
    ...


KV = """
#:kivy 2.3.0

<BaseMDNavigationItem>
    MDNavigationItemIcon:
        icon: root.icon

    MDNavigationItemLabel:
        text: root.text

MDScreen:
    BoxLayout:
        orientation: "vertical"
        MDTopAppBar:
            id: top_app_bar
            type: "small"

            MDTopAppBarLeadingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "menu"
                    on_release: app.on_menu_pressed()

            MDTopAppBarTitle:
                text: "Main Quest"
                pos_hint: {"center_x": .5, "center_y": .5}

            MDTopAppBarTrailingButtonContainer:
                MDActionTopAppBarButton:
                    icon: "dots-vertical"
                    on_release: app.on_more_pressed()

        ScrollView:    
            MDList:
                id: quest_layout

        MDNavigationBar:
            id: nav_bar
            on_switch_tabs: app.on_nav_switch(*args)

            BaseMDNavigationItem:
                icon: "trophy"
                text: "Progress"
                on_release: app.on_trophy_pressed()

            BaseMDNavigationItem:
                icon: "book"
                text: "Journal"
                active: True
                on_release: app.on_home_pressed()

            BaseMDNavigationItem:
                icon: "calendar"
                text: "Calendar"
                on_release: app.on_calendar_pressed()
"""

Exp = """
MDExpansionPanel:
    MDExpansionPanelHeader:
        MDListItem:
            id: base
            ripple_effect: False
            on_release: app.tap_expansion_chevron(root, chevron)

            MDListItemHeadlineText:
                id: name_text_field
                halign: "left"
                text: "Example Text"

            TrailingPressedIconButton:
                id: chevron
                icon: "chevron-right"
                on_release: app.tap_expansion_chevron(root, chevron)

    MDExpansionPanelContent:
        id: subtask_container
        orientation: "vertical"
        padding: "12dp", "12dp"

        MDList:
            id: subtask_list

            MDExpansionPanel:
                MDExpansionPanelHeader:
                    MDListItem:
                        id: base
                        ripple_effect: False
                        on_release: app.tap_expansion_chevron(root, chevron)

                        MDListItemHeadlineText:
                            id: name_text_field
                            halign: "left"
                            text: "Example Text"

                        TrailingPressedIconButton:
                            id: chevron
                            icon: "chevron-right"
                            on_release: app.tap_expansion_chevron(root, chevron)

                MDExpansionPanelContent:
                    id: subtask_container
                    orientation: "vertical"
                    padding: "12dp", "12dp"

                    MDList:
                        id: subtask_list

"""

class Task:
    def __init__(self, title: str, subtasks: list = None):
        self.title = title
        self.subtasks = subtasks or []

class TaskContent(MDBoxLayout):
    """Container for nested expansion panels (adaptive height)."""
    pass

class TodoApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):

        tree = Task(
            "Project",
            subtasks=[
                Task("Frontend", subtasks=[
                    Task("Login page"),
                    Task("Dashboard", subtasks=[
                        Task("Stats Widget"),
                        Task("User Profile"),
                    ]),
                ]),
                Task("Backend", subtasks=[
                    Task("Auth"),
                    Task("Database"),
                ]),
                Task("Docs"),
            ],
        )
        quest_layout = self.root.ids.quest_layout
        async def add_quests():
            for _ in range(10):
                await asynckivy.sleep(0)
                quest_widget = Builder.load_string(Exp)
                quest_layout.add_widget(quest_widget)
        asynckivy.start(add_quests())

    def tap_expansion_chevron(self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton):
        Animation(
            padding=[0, dp(12), 0, dp(12)]
            if not panel.is_open
            else [0, 0, 0, 0],
            d=0.2,
        ).start(panel)
        panel.open() if not panel.is_open else panel.close()
        panel.set_chevron_down(
            chevron
        ) if not panel.is_open else panel.set_chevron_up(chevron)

if __name__ == "__main__":
    TodoApp().run()