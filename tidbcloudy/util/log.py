import os

ENABLE_LOG = os.environ.get("TIDBCLOUDY_LOG") in {"1", "true", "on", "yes"}


def log(*args):
    """ Print log to stdout """
    if not ENABLE_LOG:
        return
    print(*args)
