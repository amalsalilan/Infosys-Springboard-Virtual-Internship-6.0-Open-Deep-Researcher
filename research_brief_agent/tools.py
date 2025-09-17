# tools.py
from datetime import datetime
from zoneinfo import ZoneInfo

def get_today_date_ist() -> str:
    """Return today's date in Asia/Kolkata as YYYY-MM-DD."""
    return datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%Y-%m-%d")
