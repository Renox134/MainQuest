from config import Config

import os
import shutil

from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.uix.colorpicker import ColorPicker
from kivy.metrics import dp

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
    from android import mActivity, api_version
    from android.permissions import request_permissions, Permission
    from jnius import autoclass

    Intent = autoclass("android.content.Intent")
    DocumentsContract = autoclass("android.provider.DocumentsContract")
    Uri = autoclass("android.net.Uri")
    Environment = autoclass("android.os.Environment")
    PythonActivity = autoclass("org.kivy.android.PythonActivity")

    IS_ANDROID = True
except ImportError:
    IS_ANDROID = False

REQUEST_CODE_PICK_FOLDER = 9901


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

        scroll_view = ScrollView(size_hint_y=None, height=dp(300))
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
            height=dp(400)
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
        self.selected_folder = None  # only used on desktop

        self.file_manager = MDFileManager(
            exit_manager=self._close_file_manager,
            select_path=self._on_folder_selected_desktop,
            selector="folder",
        )

        self.status_label = MDLabel(
            text="No folder selected",
            halign="center",
            adaptive_height=True,
        )

        def on_browse():
            if IS_ANDROID:
                self._launch_saf_picker()
            else:
                self._open_file_manager()

        def on_confirm():
            if IS_ANDROID:
                # On Android, export is triggered immediately after SAF pick,
                # but allow re-triggering if a URI is already stored
                if not hasattr(self, "_saf_uri") or self._saf_uri is None:
                    self.status_label.text = "Please select a folder first"
                    return
                self._do_export_android(self._saf_uri)
            else:
                if not self.selected_folder:
                    self.status_label.text = "Please select a folder first"
                    return
                self._do_export_desktop(self.selected_folder)

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

        # Register SAF activity result handler
        if IS_ANDROID:
            self._bind_activity_result()

    # ------------------------------------------------------------------ SAF
    def _launch_saf_picker(self):
        intent = Intent(Intent.ACTION_OPEN_DOCUMENT_TREE)
        # Pass the initial URI as a string, not a Uri object
        downloads_uri = Uri.parse(
            "content://com.android.externalstorage.documents/document/primary%3ADownloads"
        )
        intent.putExtra(DocumentsContract.EXTRA_INITIAL_URI, downloads_uri.toString())
        mActivity.startActivityForResult(intent, REQUEST_CODE_PICK_FOLDER)

    def _bind_activity_result(self):
        from android.activity import bind as android_bind
        android_bind(on_activity_result=self._on_activity_result)

    def _on_activity_result(self, request_code, result_code, intent_data):
        RESULT_OK = -1  # android.app.Activity.RESULT_OK
        if request_code != REQUEST_CODE_PICK_FOLDER:
            return
        if result_code != RESULT_OK or intent_data is None:
            self.status_label.text = "Folder selection cancelled"
            return

        uri = intent_data.getData()
        # Take persistable permission so we can write without any storage permission
        mActivity.getContentResolver().takePersistableUriPermission(
            uri,
            Intent.FLAG_GRANT_READ_URI_PERMISSION | Intent.FLAG_GRANT_WRITE_URI_PERMISSION
        )

        self._saf_uri = uri
        self.status_label.text = f"Selected: {uri.getLastPathSegment()}"
        # Export immediately after selection
        self._do_export_android(uri)

    # ------------------------------------------------------------------ Export
    def _do_export_android(self, tree_uri):
        try:
            ContentResolver = autoclass("android.content.ContentResolver")
            DocumentFile = autoclass("androidx.documentfile.provider.DocumentFile")

            resolver = mActivity.getContentResolver()
            tree = DocumentFile.fromTreeUri(mActivity, tree_uri)

            for src_path in (self.data_path, self.config_path):
                filename = os.path.basename(src_path)
                # Create or overwrite the file in the chosen folder
                existing = tree.findFile(filename)
                if existing:
                    existing.delete()
                dest_doc = tree.createFile("application/json", filename)
                dest_uri = dest_doc.getUri()

                out_stream = resolver.openOutputStream(dest_uri)
                with open(src_path, "rb") as f:
                    data = f.read()
                out_stream.write(data)
                out_stream.close()

            self.dismiss()
            MDSnackbar(MDSnackbarText(text="Files exported successfully!"), duration=3).open()

        except Exception as e:
            self.status_label.text = f"Export failed: {e}"

    def _do_export_desktop(self, folder: str):
        try:
            for src in (self.data_path, self.config_path):
                shutil.copy2(src, os.path.join(folder, os.path.basename(src)))
            self.dismiss()
            MDSnackbar(MDSnackbarText(text="Files exported successfully!"), duration=3).open()
        except Exception as e:
            self.status_label.text = f"Export failed: {e}"

    # ------------------------------------------------------------------ Desktop file manager
    def _open_file_manager(self):
        self.file_manager.show(os.path.expanduser("~"))

    def _close_file_manager(self, *args):
        self.file_manager.close()

    def _on_folder_selected_desktop(self, path: str):
        self.selected_folder = path
        self.status_label.text = f"Selected: {path}"
        self.file_manager.close()
