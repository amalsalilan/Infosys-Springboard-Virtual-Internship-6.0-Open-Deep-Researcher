import os
from dotenv import load_dotenv

def get_api_key():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing GOOGLE_API_KEY in environment variables.")
    return api_key
