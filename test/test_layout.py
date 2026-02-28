from kivy.lang import Builder
from kivy.uix.widget import Widget

from kivymd.app import MDApp
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.divider import MDDivider
from kivymd.uix.list import (
    MDListItem,
    MDListItemLeadingIcon,
    MDListItemSupportingText,
)
from kivymd.uix.scrollview import ScrollView

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDButton:
        pos_hint: {'center_x': .5, 'center_y': .5}
        on_release: app.show_alert_dialog()

        MDButtonText:
            text: "Show dialog"         
'''


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def show_alert_dialog(self):
        items = [MDListItem(
                    MDListItemLeadingIcon(
                        icon="gmail",
                    ),
                    MDListItemSupportingText(
                        text=f"Item number {i}",
                    ),
                    theme_bg_color="Custom",
                    md_bg_color=self.theme_cls.transparentColor,
                ) for i in range(10)]
        sv = ScrollView(size_hint_y=None, height=200)
        layout = MDBoxLayout(orientation='vertical', adaptive_height=True)
        sv.add_widget(layout)
        for item in items:
            layout.add_widget(item)

        MDDialog(
            # ----------------------------Icon-----------------------------
            MDDialogIcon(
                icon="refresh",
            ),
            # -----------------------Headline text-------------------------
            MDDialogHeadlineText(
                text="Reset settings?",
            ),
            # -----------------------Supporting text-----------------------
            MDDialogSupportingText(
                text="This will reset your app preferences back to their "
                "default settings. The following accounts will also "
                "be signed out:",
            ),
            # -----------------------Custom content------------------------
            MDDialogContentContainer(
                MDDivider(),
                sv,  # add the ScrollView to the dialog content container...
                MDDivider(),
                orientation="vertical",
            ),
            # ---------------------Button container------------------------
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                ),
                MDButton(
                    MDButtonText(text="Accept"),
                    style="text",
                ),
                spacing="8dp",
            ),
            # -------------------------------------------------------------
        ).open()


Example().run()