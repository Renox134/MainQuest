from typing import Any

from model.quest_log import QuestLog
from ui.widgets.quest_widget import QuestWidget, MDExpansionPanel, LeadingPressedIconButton

from kivy.core.window import Window
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.animation import Animation
from kivy.properties import StringProperty
from kivymd.app import MDApp
from kivymd.uix.navigationbar import MDNavigationItem

Window.size = (350, 650)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


base_app_kv = """
<BaseMDNavigationItem>

    MDNavigationItemIcon:
        icon: root.icon

    MDNavigationItemLabel:
        text: root.text

MDScreen:
    md_bg_color: self.theme_cls.secondaryContainerColor

    GridLayout:
        cols: 1
        rows: 3
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
                halign: "center"

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


class MainQuestApp(MDApp):
    """
    The main app.
    """

    def __init__(self, quest_log: QuestLog, **kwargs: Any):
        self.quest_log = quest_log
        super().__init__(**kwargs)

    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_string(base_app_kv)

    def on_start(self):
        """Populate quest widgets dynamically after layout is built."""
        quest_layout = self.root.ids.quest_layout
        for _ in range(10):
            quest_layout.add_widget(QuestWidget(self.quest_log.quests[0]).root)
        # for quest in self.quest_log.quests:
        #     quest_widget = QuestWidget(quest)
        #     quest_layout.add_widget(quest_widget.root)

    def on_menu_pressed(self, *args):
        self.root.ids.top_app_bar.do_layout()
        print("menu pressed")

    def on_more_pressed(self, *args):
        print("three dots pressed")

    def on_nav_switch(self, *args):
        print("Called")

    def on_calendar_pressed(self, *args):
        print("Calendar pressed")

    def on_home_pressed(self, *args):
        print("Home pressed")

    def on_trophy_pressed(self, *args):
        print("Trophy pressed")

    def tap_expansion_chevron(self, panel: MDExpansionPanel, chevron: LeadingPressedIconButton):
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
