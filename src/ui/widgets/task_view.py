from model.task import Task

from kivymd.uix.bottomsheet import MDBottomSheet
from kivymd.uix.pickers import MDDockedDatePicker, MDModalInputDatePicker, MDModalDatePicker
from kivy.metrics import dp
from kivy.lang.builder import Builder


Builder.load_file("ui/widgets/task_view.kv")


class TaskView(MDBottomSheet):
    def __init__(self, task: Task | None = None, *args, **kwargs):
        self.task: Task | None = task
        super().__init__(*args, **kwargs)
        self.bind(on_close=self.remove_widget_when_closed)

        # set state of the widget to task
        if self.task.notes is not None:
            self.ids.notes_field.text = task.notes

    def show_date_picker(self, focus):
        
        if not focus:
            return

        date_dialog = MDDockedDatePicker()
        # You have to control the position of the date picker dialog yourself.
        date_dialog.pos = [
            self.ids.date_field.center_x - date_dialog.width / 2,
            self.ids.date_field.y - (date_dialog.height - dp(320)),
        ]
        date_dialog.open()

    def show_date_picker(self):
        date_dialog = MDModalDatePicker()
        date_dialog.open()

    def remove_widget_when_closed(self, widget):
        """Removes the widget when closed, such that it doesn't stay around.

        Args:
            widget (_type_): The task view widget to remove.
        """
        widget.parent.remove_widget(widget)
