from kivy.lang import Builder
from kivymd.app import MDApp


from kivymd.uix.list import MDList, MDListItem
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationbar import MDNavigationItem
from kivymd.uix.button import MDIconButton
from kivy.properties import StringProperty
from kivy.core.window import Window


Window.size = (350, 650)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


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
        # Build example nested data
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


if __name__ == "__main__":
    TodoApp().run()