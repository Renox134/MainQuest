from kivy.resources import resource_find

from journal import Journal
from ui.app import MainQuestApp

if __name__ == "__main__":
    controller: Journal = Journal()

    main_log_path = resource_find("main_quest.json")
    controller.import_journal(main_log_path)
    main_app = MainQuestApp(controller, main_log_path)

    main_app.run()
