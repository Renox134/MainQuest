from kivy.resources import resource_find
import json

from typing import Any


class Config():
    """
    Reads in the config information from the config json.
    """

    @staticmethod
    def get(key: str) -> Any:
        config_path = resource_find("config.json")
        # if resource find doesn't find anything, try default path
        if config_path is None:
            config_path = "./src/config.json"
        with open(config_path, "r") as file:
            config_dict = json.load(file)
            if key not in config_dict.keys():
                raise KeyError(f"The config does not contain the entered key: {key}")
            else:
                return config_dict[key]
