from datetime import datetime


def time_in_millis() -> int:
    return int(datetime.now().timestamp() * 1000)
