from model.task import Task
from model.quest import Quest

import json


if __name__ == "__main__":
    with open("test/test_quest.json", "r", encoding="utf-8") as file:
        d = json.load(file)
        print(d)
        q_1_import: Quest = Quest.to_quest(d)
