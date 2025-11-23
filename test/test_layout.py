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
from kivymd.uix.divider import MDDivider
from kivymd.uix.label import MDLabel
from kivymd.uix.expansionpanel import *
import asynckivy
from kivy.properties import StringProperty
from kivy.core.window import Window


Window.size = (350, 650)


class BaseMDNavigationItem(MDNavigationItem):
    icon = StringProperty()
    text = StringProperty()


class ExpansionPanelItem(MDExpansionPanel):
    ...


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

<ExpansionPanelItem>
    adaptive_height: True

    MDExpansionPanelHeader:

        MDListItem:
            theme_bg_color: "Custom"
            md_bg_color: self.theme_cls.surfaceContainerLowColor
            ripple_effect: False

            MDListItemLeadingIcon:
                icon: "checkbox-blank-circle"

            MDListItemHeadlineText:
                text: "Task description"

            MDListItemSupportingText:
                text: "Note"

            MDListItemTertiaryText:
                text: "datetime"

            TrailingPressedIconButton:
                id: chevron
                icon: "chevron-right"
                on_release: app.tap_expansion_chevron(root, chevron)

    MDExpansionPanelContent:
        id: expansion_content
        orientation: "vertical"
        padding: "12dp", 0, "12dp", "12dp"
        md_bg_color: self.theme_cls.surfaceContainerLowestColor

        MDLabel:
            text: "Channel information"
            adaptive_height: True
            padding: "16dp", "12dp"

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

class TodoApp(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def on_start(self):
        quest_layout = self.root.ids.quest_layout
        async def add_quests():
            for _ in range(10):
                await asynckivy.sleep(0)
                quest_widget = ExpansionPanelItem()
                quest_widget.ids.expansion_content.add_widget(ExpansionPanelItem())
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