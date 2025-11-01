from model.quest_log import QuestLog


if __name__ == "__main__":
    main_log: QuestLog = QuestLog()

    main_log.import_quests("main_quest.json")
    for quest in main_log.quests:
        print(quest)
