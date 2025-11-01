from model.task import Task
from model.quest import Quest


if __name__ == "__main__":
    objectives = []

    for i in range(10):
        objectives.append(Task("Objective " + str(i)))

    q = Quest(objectives, "Test Quest")
