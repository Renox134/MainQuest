from typing import Any, Optional
import json

DATA = {}


class Config():
    """
    Reads in the config information from the config json.
    """
    @staticmethod
    def load_data(path: str) -> None:
        with open(path, "r", encoding="utf8") as file:
            tmp = json.load(file)

        for key, val in tmp.items():
            DATA[key] = val

    @staticmethod
    def get(key: str, default: Optional[Any] = None) -> Any:
        if key not in DATA.keys():
            return default
        else:
            return DATA[key]
        
    def store(key: str, value: Any) -> None:
        DATA[key] = value
        
    def save(path: str) -> None:
        with open(path, "w", encoding="utf8") as file:
            json.dump(DATA, file, indent=4)
