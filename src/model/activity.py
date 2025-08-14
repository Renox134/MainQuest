import datetime
from model.objective import Objective


class Activity:
    """
    Class representing an activity.
    """
    def __init__(self, objective: Objective, name: str, status: float = 0.0,
                 date: datetime.date | None = None,
                 time: datetime.time | None = None, duration: int = 0):

        self.objective: Objective = objective
        self.name: str = name
        self.status = status
        self.date: datetime.date | None = date
        self.time: datetime.time | None = time
        self.duration: int = duration

    def set_status(self, status: float) -> None:
        self.status = status
