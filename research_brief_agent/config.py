# config.py
import os
from dotenv import load_dotenv

load_dotenv()

def get_env(key: str, default=None):
    val = os.getenv(key, default)
    if val is None:
        return default
    return val
