from model.quest import Quest
from kivymd.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemLeadingIcon
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.properties import StringProperty


KV='''
<ExpansionPanelItem>

    MDExpansionPanelHeader:

        MDListItem:
            ripple_effect: False

            MDListItemSupportingText:
                id: "name_text_field"
                halign: "center"
                text: root.text

            LeadingPressedIconButton:
                id: chevron
                icon: "chevron-right"
                on_release: app.tap_expansion_chevron(root, chevron)

    MDExpansionPanelContent:
        id: task_container
        orientation: "vertical"
        padding: "12dp", 0, "12dp", "12dp"

        MDLabel:
            text: "Here should be the actual tasks"
            adaptive_height: True
            padding_x: "16dp"
            padding_y: "12dp"

BoxLayout:
    MDList:
        id: list_container

'''


class ExpansionPanelItem(MDExpansionPanel):
    text = StringProperty()


class LeadingPressedIconButton(
    ButtonBehavior, RotateBehavior, MDListItemLeadingIcon
):
    ...

class QuestWidget:
    """
    A widget used to display a quest.
    """

    def __init__(self, quest: Quest):
        self.quest: Quest = quest
        self.root: BoxLayout = Builder.load_string(KV)

        self.__build()

    def __build(self) -> None:
        main_panel = ExpansionPanelItem()
        main_panel.text = self.quest.name
        self.root.ids.list_container.add_widget(main_panel)
        # self.root.ids.name_text_field.text = self.quest.name

        # task_container: BoxLayout = BoxLayout(orientation="vertical")

        # for task in self.quest.tasks:
        #     task_container.add_widget(MDLabel(text=task.description))
        
        # self.root.add_widget(task_container)


    def tap_expansion_chevron(
        self, panel: MDExpansionPanel, chevron: LeadingPressedIconButton
    ):
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
