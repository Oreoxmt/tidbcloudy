import datetime


def timestamp_to_string(timestamp: int) -> str:
    """
    Convert timestamp to datetime string.
    Args:
        timestamp:

    Returns:

    """
    if timestamp is None:
        return ""
    return datetime.datetime.fromtimestamp(timestamp).isoformat()
