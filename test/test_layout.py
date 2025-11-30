from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.bottomsheet import MDBottomSheet

KV = '''
MDScreen:
    md_bg_color: self.theme_cls.backgroundColor

    MDButton:
        pos_hint: {"center_x": .5, "center_y": .5}
        on_release: app.open_sheet()

        MDButtonText:
            text: "Open sheet"

    MDBottomSheet:
        id: bottom_sheet
        size_hint_y: None
        height: "84dp"

        MDBottomSheetDragHandle:

            MDBottomSheetDragHandleTitle:
                text: "MDBottomSheet"
                adaptive_height: True
                pos_hint: {"center_y": .5}

            MDBottomSheetDragHandleButton:
                icon: "close"
                on_release: app.close_sheet()
'''


class Example(MDApp):
    def build(self):
        return Builder.load_string(KV)
    
    def open_sheet(self) -> None:
        print("Open sheet")
        sheet: MDBottomSheet = self.root.ids.bottom_sheet
        sheet.set_state("toggle")

    def close_sheet(self) -> None:
        print("Close sheet")
        sheet: MDBottomSheet = self.root.ids.bottom_sheet
        sheet.set_state("toggle")


Example().run()
