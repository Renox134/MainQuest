from model.quest import Quest
from kivymd.uix.boxlayout import BoxLayout
from kivy.lang.builder import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import RotateBehavior
from kivy.uix.behaviors import ButtonBehavior
from kivymd.uix.expansionpanel import MDExpansionPanel
from kivymd.uix.list import MDListItemLeadingIcon
from kivy.properties import StringProperty


KV='''
<ExpansionPanelItem>

    MDExpansionPanelHeader:

        MDListItem:
            ripple_effect: False

            MDListItemSupportingText:
                id: name_text_field
                halign: "center"
                text: root.text

            LeadingPressedIconButton:
                id: chevron
                icon: "chevron-right"
                pos_hint: {"center_x": .1, "center_y": .5}
                on_release: app.tap_expansion_chevron(root, chevron)

    MDExpansionPanelContent:
        id: task_container
        orientation: "vertical"
        padding: "12dp", 0, "12dp", "12dp"

ExpansionPanelItem:

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

        self.__build()

    def __build(self) -> None:
        self.root = Builder.load_string(KV)
        self.root.text = self.quest.name
        task_container = self.root.ids.task_container

        for task in self.quest.tasks:
            task_container.add_widget(MDLabel(text=task.description))
