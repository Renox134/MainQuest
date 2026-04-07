from typing import Any
import json

DATA = {}


class Config():
    """
    Reads in the config information from the config json.
    """
    @staticmethod
    def load_data(path: str) -> None:
        with open(path, "r") as file:
            tmp = json.load(file)

        for key, val in tmp.items():
            DATA[key] = val

    @staticmethod
    def get(key: str) -> Any:
        if key not in DATA.keys():
            raise KeyError(f"The config does not contain the entered key: {key}. " +
                           f"Known keys: {[k for k in DATA.keys()]}")
        else:
            return DATA[key]
