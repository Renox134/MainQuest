from model.objective import Objective
from model.quest import Quest


if __name__ == "__main__":
    objectives = []

    for i in range(10):
        objectives.append(Objective("Objective " + str(i)))

    q = Quest(objectives, "Test Quest")
    o = Objective("test")
    print(o.to_dict())
