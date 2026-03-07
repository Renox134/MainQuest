from controller import Controller
from object_parser import ObjectParser
from ui.app import MainQuestApp

if __name__ == "__main__":
    controller: Controller = Controller()
    parser: ObjectParser = ObjectParser()

    controller.import_quests("main_quest.json")
    parser.init(controller.quests)
    main_app = MainQuestApp(controller)

    main_app.run()
