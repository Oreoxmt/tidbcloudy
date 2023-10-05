from datetime import datetime, tzinfo
from typing import Union


def timestamp_to_string(timestamp: Union[int, None], timezone: tzinfo = None) -> str:
    """
    Convert timestamp to datetime string.
    Args:
        timestamp: the timestamp to convert.
        timezone: the timezone to use.

    Returns:
        the datetime string in format of YYYY-MM-DD HH:MM:SS.

    """
    if timestamp is None:
        return ""

    return datetime.fromtimestamp(timestamp, tz=timezone).strftime("%Y-%m-%d %H:%M:%S")


def get_current_year_month(timezone: tzinfo = None) -> str:
    """
    Get current year and month.
    Args:
        timezone: the timezone to use.
    Returns:
        the year and month string in format of YYYY-MM.

    """
    return datetime.now(tz=timezone).strftime("%Y-%m")
