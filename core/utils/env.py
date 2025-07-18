import math
import sys
import importlib

SQUARE_SIZE = 10
R_VIEW = SQUARE_SIZE * math.sqrt(2) / 2
SEED_CORDS = (SQUARE_SIZE / 2, SQUARE_SIZE / 2, 0)
DISCOVERY_INTERVAL = 30
LOAD_REPORT_INTERVAL = 10
RECONNECT_GRACE_PERIOD = 60
TIMEOUT = 60
CONNECTION_QUEUE_LIMIT = 10
HANDSHAKE_GRACE_PERIOD = 5

def load_env(path: str):
    global TIMEOUT, SQUARE_SIZE, CONNECTION_QUEUE_LIMIT, HANDSHAKE_GRACE_PERIOD

    spec = importlib.util.spec_from_file_location("env", path)
    env = importlib.util.module_from_spec(spec)
    sys.modules["env"] = env
    spec.loader.exec_module(env)

    TIMEOUT = getattr(env, "TIMEOUT", TIMEOUT)
    SQUARE_SIZE = getattr(env, "SQUARE_SIZE", SQUARE_SIZE)
    CONNECTION_QUEUE_LIMIT = getattr(env, "CONNECTION_QUEUE_LIMIT", CONNECTION_QUEUE_LIMIT)
    HANDSHAKE_GRACE_PERIOD = getattr(env, "HANDSHAKE_GRACE_PERIOD", HANDSHAKE_GRACE_PERIOD)
