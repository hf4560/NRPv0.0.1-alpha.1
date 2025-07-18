import platform
import os
import locale
import time
import secrets
import psutil
from blake3 import blake3

def generate_hash() -> str:
    return get_blake3_hash(get_salt(32) + get_info())

def get_blake3_hash(data: bytes) -> str:
    return blake3(data).hexdigest()

def get_salt(n: int) -> bytes:
    return get_blake3_hash(secrets.token_bytes(n)).encode()

def get_info() -> bytes:
    uname = platform.uname()
    info = (
        (platform.machine() or "unknown")
        + (platform.node() or os.uname().nodename)
        + platform.system() + platform.version()
        + f"{uname.system}{uname.machine}" + uname.system
        + (locale.getlocale()[0] or "unknown")
        + time.tzname[0]
        + str(psutil.cpu_count(logical=True))
        + str(round(psutil.virtual_memory().total / (1024 ** 3), 2))
    )
    return info.encode()
