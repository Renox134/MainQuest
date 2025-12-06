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

                MDButton:
                    pos_hint: {"center_x": .5, "center_y": .5}
                    on_release: app.show_bottom_sheet()

                    MDButtonText:
                        text: "Open Bottom Sheet"

                    MDButtonIcon:
                        icon: "plus"
        MDBottomSheet:
            id: bottom_sheet
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
                        icon: "calendar"

                    MDTextFieldMaxLengthText:
                        max_text_length: 10
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_string(KV)
    
    def on_start(self):
        self.bs = self.root.ids.bottom_sheet
        self.bs.bind(on_close=self.remove_widget_when_closed)
        self.remove_widget_when_closed(self.bs)


    def show_bottom_sheet(self):
        self.root.add_widget(self.bs)
        self.root.ids.bottom_sheet.set_state("toggle")

    def remove_widget_when_closed(self, widget):
        """Removes the widget when closed, such that it doesn't stay around.

        Args:
            widget (_type_): The task view widget to remove.
        """
        widget.parent.remove_widget(widget)

Example().run()