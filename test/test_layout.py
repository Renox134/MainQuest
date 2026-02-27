from kivy.lang import Builder
from kivy.core.window import Window


from kivymd.app import MDApp
from kivymd.uix.list import MDListItem, MDListItemHeadlineText


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

                MDList:
                    id: main_list
                    MDListItem:
                        MDListItemHeadlineText:
                            text: "origin_test"
'''


class Example(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Olive"
        return Builder.load_string(KV)
    
    def on_start(self):
        lst = self.root.ids.main_list
        for i in range(2):
            lst.add_widget(MDListItem(MDListItemHeadlineText(text="from_base_class")))


Example().run()