import time
from core.utils.env import RECONNECT_GRACE_PERIOD

recent_reconnects = {}

def can_reconnect(client_id: str) -> bool:
    now = time.time()
    last_time = recent_reconnects.get(client_id, 0)
    if now - last_time < RECONNECT_GRACE_PERIOD:
        return False
    recent_reconnects[client_id] = now
    return True
