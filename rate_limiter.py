from datetime import datetime, timedelta
from collections import defaultdict

_calls = defaultdict(list)
MAX_CALLS = 5
WINDOW = timedelta(minutes=1)

def allow(ip: str) -> bool:
    now = datetime.utcnow()
    timestamps = _calls[ip]
    _calls[ip] = [t for t in timestamps if now - t < WINDOW]
    if len(_calls[ip]) >= MAX_CALLS:
        return False
    _calls[ip].append(now)
    return True
