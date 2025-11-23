import json

from typing import Any

class Config():
    """
    Reads in the config information from the config json.
    """

    @staticmethod
    def get(key: str) -> Any:
        with open("src/config.json", "r") as file:
            config_dict = json.load(file)
            if key not in config_dict.keys():
                raise KeyError(f"The config does not a the entered key: {key}")
            else:
                return config_dict[key]