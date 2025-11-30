from model.task import Task

from kivymd.uix.bottomsheet import MDBottomSheet
from kivy.lang.builder import Builder


Builder.load_file("ui/widgets/task_view.kv")


class TaskView(MDBottomSheet):
    def __init__(self, task: Task | None = None, *args, **kwargs):
        self.task: Task | None = task
        super().__init__(*args, **kwargs)
        self.bind(on_close=self.remove_widget_when_closed)

    def remove_widget_when_closed(self, widget):
        """Removes the widget when closed, such that it doesn't stay around.

        Args:
            widget (_type_): The task view widget to remove.
        """
        widget.parent.remove_widget(widget)
