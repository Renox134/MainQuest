from kivy.resources import resource_find

from journal import Journal
from object_parser import ObjectParser
from ui.app import MainQuestApp

if __name__ == "__main__":
    controller: Journal = Journal()
    parser: ObjectParser = ObjectParser()

    main_log_path = resource_find("main_quest.json")
    controller.import_journal(main_log_path)
    # parser.init(controller.quests)
    main_app = MainQuestApp(controller, main_log_path)

    main_app.run()
