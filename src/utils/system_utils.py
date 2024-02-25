from datetime import datetime


def time_in_millis() -> int:
    """
    Get the current time in milliseconds.

    :return: The current time in milliseconds.
    """
    return int(datetime.now().timestamp() * 1000)
