# configurations.py

import os
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain.chat_models import init_chat_model
from tavily import TavilyClient

# Load environment variables
load_dotenv()

# Apply keys from .env
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Rate limiter setup
rate_limiter = InMemoryRateLimiter(
    requests_per_second=0.083,   # ~5 requests per minute
    check_every_n_seconds=0.1,
    max_bucket_size=1
)

# Models
model = init_chat_model("gemini-2.5-pro", model_provider="google_genai", temperature=0, rate_limiter=rate_limiter)
summarization_model = init_chat_model("gemini-2.5-pro", model_provider="google_genai", temperature=0, rate_limiter=rate_limiter)
compress_model = init_chat_model("gemini-2.5-pro", model_provider="google_genai", temperature=0, rate_limiter=rate_limiter)

# Tavily client
tavily_client = TavilyClient()

# Utility functions
def get_today_str() -> str:
    """Get current date in a human-readable format."""
    return datetime.now().strftime("%a %b %#d, %Y")

def get_current_dir() -> Path:
    """Get current directory of the module (works in notebooks & scripts)."""
    try:
        return Path(_file_).resolve().parent
    except NameError:
        return Path.cwd()