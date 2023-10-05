import json
import os


def load_config(filename: str = "mock_config.json"):
    with open(f"{os.path.dirname(__file__)}/{filename}", "r") as f:
        return json.load(f)


CONFIG = load_config()
