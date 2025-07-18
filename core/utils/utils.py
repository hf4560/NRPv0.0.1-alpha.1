import os

def get_env_var(name: str, default: str = "") -> str:
    return os.getenv(name, default)
