from kivy.uix.recycleview import RecycleView
from typing import List
from model.quest import Quest
from kivy.factory import Factory


class QuestListView(RecycleView):
    """
    Scrollable list view for the quest list.
    """
    def __init__(self, quests: List[Quest], **kwargs):
        super().__init__(**kwargs)
        self.data = [
            {"name": q.name, "status": q.status} for q in quests
        ]


Factory.register("QuestListView", cls=QuestListView)
