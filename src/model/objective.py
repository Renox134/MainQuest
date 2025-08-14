from typing import Dict, Any


class Objective:
    """
    A class representing an objective that is to be completed.
    """
    def __init__(self, description: str, status: float = 0.0):
        self.description: str = description
        self.status: float = status

    def set_status(self, status: float) -> None:
        self.status = status

    def __str__(self):
        return "Description: \t" + self.description + "\tStatus:\t\t" + str(self.status) + "\n"

    def to_dict(self) -> Dict[str, Any]:
        return {"Description": self.description, "Status": self.status}

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Objective):
            return NotImplemented
        return (
            self.description == other.description
            and round(self.status, 2) == round(other.status, 2)
        )
