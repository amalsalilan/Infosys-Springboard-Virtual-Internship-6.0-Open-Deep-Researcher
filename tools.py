import re
from datetime import datetime
from zoneinfo import ZoneInfo

# Date utility
def get_date_today() -> str:
    """Return today's date in Kolkata timezone formatted as 'DD Mon YYYY'"""
    time = ZoneInfo("Asia/Kolkata")
    return datetime.now(time).strftime("%d %b %Y")

# JSON extraction utility
def extract_json(text: str) -> str:
    """Extract JSON object from text (removes markdown fences if present)."""
    match = re.search(r"(\{.*\})", text, re.DOTALL)
    if match:
        return match.group(1)
    return text.strip()
