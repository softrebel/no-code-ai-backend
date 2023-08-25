from datetime import datetime, timezone


def get_now_timestamp():
    now = datetime.now(timezone.utc)
    return now.timestamp()
