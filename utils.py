import random, string
import re
from urllib.parse import urlparse
from datetime import datetime

CODE_LENGTH = 6
ALPHABET = string.ascii_letters + string.digits

def generate_code(n=CODE_LENGTH):
    return ''.join(random.choice(ALPHABET) for _ in range(n))

def is_valid_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https") and bool(parsed.netloc)
    except:
        return False

def now_iso():
    return datetime.utcnow().isoformat() + "Z"
