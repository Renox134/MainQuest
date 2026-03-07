from controller import Controller
from ui.app import MainQuestApp

if __name__ == "__main__":
    controller: Controller = Controller()

    controller.import_quests("main_quest.json")
    main_app = MainQuestApp(controller)

    main_app.run()
