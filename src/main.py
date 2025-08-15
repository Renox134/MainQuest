from model.quest_log import QuestLog

from gui.quest_app import QuestApp


def main() -> None:
    quest_log: QuestLog = QuestLog()
    quest_log.import_quests("main_quest.json")

    QuestApp(quest_log).run()


if __name__ == "__main__":
    main()
