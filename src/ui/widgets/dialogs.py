from config import Config

from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.colorpicker import ColorPicker

from kivymd.app import MDApp
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, \
    MDDialogSupportingText, MDDialogContentContainer
from kivymd.uix.button import MDIconButton
from kivymd.uix.boxlayout import MDBoxLayout


class ConfirmDialog(MDDialog):
    def __init__(self, heading: str, supporting_text: str, confirm_func, *args, **kwargs):
        self.heading = heading
        self.supporting_text = supporting_text
        self.confirm_func = confirm_func
        super().__init__(*args, **kwargs)

        def confirm():
            self.dismiss()
            confirm_func()

        self.add_widget(MDDialogHeadlineText(text=heading))
        self.add_widget(MDDialogSupportingText(text=supporting_text))
        self.add_widget(MDDialogButtonContainer(
            Widget(),
            MDIconButton(icon="check", on_release=lambda x: confirm()),
            MDIconButton(icon="close", on_release=lambda x: self.dismiss())
        ))


class ThemeSelectDialog(MDDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.selected_theme = None

        color_options = [
            "Red", "Pink", "Purple", "Indigo",
            "Navy", "Blue", "Lightblue", "Cyan", "Teal",
            "Green", "Lightgreen", "Olive", "Lime",
            "Yellow", "Orange", "Orangered",
            "Brown", "Gray"
        ]

        def on_item_press(item, color):
            MDApp.get_running_app().theme_cls.primary_palette = color
            MDApp.get_running_app().root.ids.main_color_theme_text.text = "Main Theme: " + color
            Config.store("primary_palette", color)
            self.dismiss()

        scroll_view = ScrollView(size_hint_y=None, height=300)
        color_list_layout = MDBoxLayout(orientation='vertical', adaptive_height=True)

        for color in color_options:
            item = MDListItem(
                MDListItemLeadingIcon(icon="palette", icon_color=color.lower(), theme_icon_color="Custom"),
                MDListItemHeadlineText(text=color, text_color=color.lower(), theme_text_color="Custom"),
                on_release=lambda x, c=color: on_item_press(x, c),
            )
            color_list_layout.add_widget(item)

        scroll_view.add_widget(color_list_layout)

        self.add_widget(MDDialogHeadlineText(text="Select Main Theme"))
        self.add_widget(MDDialogContentContainer(scroll_view))
        self.add_widget(MDDialogButtonContainer(
            Widget(),
            MDIconButton(icon="close", on_release=lambda x: self.dismiss())
        ))


class ColorPickerDialog(MDDialog):
    def __init__(self, on_confirm=None, initial_color=(1, 1, 1, 1), *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.on_confirm_callback = on_confirm

        def confirm():
            if self.on_confirm_callback:
                self.on_confirm_callback(self.color_picker.color)
            self.dismiss()

        self.color_picker = ColorPicker(
            color=initial_color,
            size_hint_y=None,
            height=400
        )

        self.add_widget(MDDialogHeadlineText(text="Select Color"))
        self.add_widget(MDDialogContentContainer(
            self.color_picker,
            orientation="vertical"
        ))
        self.add_widget(MDDialogButtonContainer(
            Widget(),
            MDIconButton(icon="check", on_release=lambda x: confirm()),
            MDIconButton(icon="close", on_release=lambda x: self.dismiss())
        ))
