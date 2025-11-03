from model.quest_log import QuestLog
from ui.app import MainQuestApp


if __name__ == "__main__":
    main_log: QuestLog = QuestLog()

    main_log.import_quests("main_quest.json")
    main_app = MainQuestApp(main_log)

    main_app.run()
