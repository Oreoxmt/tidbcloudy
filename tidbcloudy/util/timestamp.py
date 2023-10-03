import datetime


def timestamp_to_string(timestamp: int) -> str:
    """
    Convert timestamp to datetime string.
    Args:
        timestamp:

    Returns:
        the datetime string.

    """
    if timestamp is None:
        return ""
    return datetime.datetime.fromtimestamp(timestamp).isoformat()


def get_current_year_month() -> str:
    """
    Get current year and month.
    Returns:
        the year and month string in format of YYYY-MM.

    """
    return datetime.datetime.now().strftime("%Y-%m")
