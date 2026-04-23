from typing import Any, Optional
import json
import os
import tempfile

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

    @staticmethod
    def store(key: str, value: Any) -> None:
        DATA[key] = value

    @staticmethod
    def save(path: str) -> None:
        dir_name = os.path.dirname(path)

        with tempfile.NamedTemporaryFile("w", dir=dir_name, delete=False, suffix=".tmp") as tmp:
            json.dump(DATA, tmp, indent=4)
            tmp_path = tmp.name

        os.replace(tmp_path, path)
