# quest_detail_screen.py
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty
from kivy.factory import Factory
from kivy.uix.label import Label
from kivy.metrics import dp


class QuestDetailScreen(BoxLayout):
    quest_name = StringProperty("")
    objectives = ListProperty([])

    def populate(self, quest):
        self.quest_name = quest.name
        self.ids.objectives_container.clear_widgets()
        for desc, completed in [(o.description, o.status >= 100) for o in quest.objectives]:
            lbl = Label(text=f"[s]{desc}[/s]" if completed else desc,
                        markup=True,
                        size_hint_y=None,
                        height=dp(30))
            self.ids.objectives_container.add_widget(lbl)


Factory.register("QuestDetailScreen", cls=QuestDetailScreen)
