from config import Config

import os
import shutil

from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.colorpicker import ColorPicker

from kivymd.app import MDApp
from kivymd.uix.list import MDListItem, MDListItemLeadingIcon, MDListItemHeadlineText
from kivymd.uix.dialog import MDDialog, MDDialogButtonContainer, MDDialogHeadlineText, \
    MDDialogSupportingText, MDDialogContentContainer
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.textfield import MDTextField, MDTextFieldMaxLengthText, MDTextFieldHelperText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.filemanager import MDFileManager
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.label import MDLabel

try:
    from android.permissions import request_permissions, Permission
    from android import mActivity
    from jnius import autoclass

    IS_ANDROID = True
except ImportError:
    IS_ANDROID = False


class ConfirmDialog(MDDialog):
    def __init__(self, heading: str, supporting_text: str, confirm_func, *args, **kwargs):
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
                MDListItemLeadingIcon(icon="palette", icon_color=color.lower(),
                                      theme_icon_color="Custom"),
                MDListItemHeadlineText(text=color, text_color=color.lower(),
                                       theme_text_color="Custom"),
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


class NumericTextField(MDTextField):
    def insert_text(self, substring, from_undo=False):
        filtered = ''.join(c for c in substring if c.isdigit())
        super().insert_text(filtered, from_undo=from_undo)


class NumberSelectDialog(MDDialog):
    def __init__(self, current: str, max_digits: int, confirm_func, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_field = NumericTextField(
            MDTextFieldHelperText(text="Only digits are allowed", mode="on_error"),
            MDTextFieldMaxLengthText(max_text_length=max_digits),
            mode="filled",
            text=current,
        )

        def confirm():
            self.dismiss()
            confirm_func(self.text_field.text)

        self.add_widget(MDDialogHeadlineText(text="Select Number"))
        self.add_widget(MDDialogContentContainer(self.text_field))
        self.add_widget(MDDialogButtonContainer(
            Widget(),
            MDIconButton(icon="check", on_release=lambda x: confirm()),
            MDIconButton(icon="close", on_release=lambda x: self.dismiss())
        ))


class ExportDialog(MDDialog):
    def __init__(self, data_path: str, config_path: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data_path = data_path
        self.config_path = config_path
        self.selected_folder = None

        self.file_manager = MDFileManager(
            exit_manager=self._close_file_manager,
            select_path=self._on_folder_selected,
            selector="folder",
        )

        self.status_label = MDLabel(
            text="No folder selected",
            halign="center",
            adaptive_height=True,
        )

        def on_browse():
            if IS_ANDROID:
                request_permissions(
                    [Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE],
                    lambda perms, grants: self._open_file_manager() if all(grants) else None
                )
            else:
                self._open_file_manager()

        def on_confirm():
            if not self.selected_folder:
                self.status_label.text = "Please select a folder first"
                return
            self._do_export()

        self.add_widget(MDDialogHeadlineText(text="Export Data Files"))
        self.add_widget(MDDialogContentContainer(
            MDBoxLayout(
                MDLabel(
                    text=(
                        "Select a destination folder to export:\n"
                        "  • main_quest.json\n"
                        "  • config.json\n\n"
                        "Files are normally stored in the app's private\n"
                        "data directory and not directly accessible\n"
                        "via a file browser."
                    ),
                    adaptive_height=True,
                ),
                self.status_label,
                MDButton(
                    MDButtonText(text="Browse"),
                    on_release=lambda x: on_browse(),
                    style="tonal",
                ),
                orientation="vertical",
                adaptive_height=True,
                spacing="12dp",
                padding="4dp",
            )
        ))
        self.add_widget(MDDialogButtonContainer(
            Widget(),
            MDIconButton(icon="check", on_release=lambda x: on_confirm()),
            MDIconButton(icon="close", on_release=lambda x: self.dismiss()),
        ))

    def _open_file_manager(self):
        start = "/sdcard" if IS_ANDROID else os.path.expanduser("~")
        self.file_manager.show(start)

    def _close_file_manager(self, *args):
        self.file_manager.close()

    def _on_folder_selected(self, path: str):
        self.selected_folder = path
        self.status_label.text = f"Selected: {path}"
        self.file_manager.close()

    def _do_export(self):
        try:
            for src in (self.data_path, self.config_path):
                filename = os.path.basename(src)
                dst = os.path.join(self.selected_folder, filename)
                shutil.copy2(src, dst)

            self.dismiss()
            MDSnackbar(
                MDSnackbarText(text="Files exported successfully!"),
                duration=3,
            ).open()

        except Exception as e:
            self.status_label.text = f"Export failed: {e}"
