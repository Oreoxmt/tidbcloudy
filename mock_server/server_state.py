import json
import os
from typing import Any, Dict


def load_config(filename: str = "mock_config.json") -> Dict[str, Any]:
    """
    Load a configuration file in JSON format.

    Args:
        filename (str): The name of the configuration file.

    Returns:
        dict: A dictionary containing the configuration parameters.
    """
    try:
        with open(f"{os.path.dirname(__file__)}/{filename}", "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Configuration file '{filename}' not found in '{os.path.dirname(__file__)}'."
        )
    except json.JSONDecodeError:
        raise ValueError(f"Fail to decode {filename}")


CONFIG = load_config()
