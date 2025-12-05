from kivy.lang import Builder
from kivy.core.window import Window

from kivymd.app import MDApp

Window.size = (350, 650)

KV = '''
MDScreen:
    id: global_root
    MDNavigationLayout:
        id: global_nav_layout
        MDScreenManager:
            id: outer_screen_manager
            MDScreen:
                md_bg_color: self.theme_cls.backgroundColor
'''

KV2="""
MDBottomSheet:
    size_hint_y: 0.5
    size_hint_x: 1.0

    MDBottomSheetDragHandle:

    MDGridLayout:
        theme_bg_color: "Custom"
        md_bg_color: "#680606ff"
        cols: 1
        rows: 5
        orientation: "tb-lr"

        MDTextField:
            mode: "filled"

            MDTextFieldLeadingIcon:
                icon: "account"

            MDTextFieldHintText:
                text: "Filled"

            MDTextFieldHelperText:
                text: "Helper text"
                mode: "persistent"

            MDTextFieldTrailingIcon:
                icon: "information"

            MDTextFieldMaxLengthText:
                max_text_length: 10
"""


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_string(KV)
    
    def on_start(self):
        bottom_sheet = Builder.load_string(KV2)
        nav = self.root.ids.global_nav_layout
        nav.add_widget(bottom_sheet)


Example().run()