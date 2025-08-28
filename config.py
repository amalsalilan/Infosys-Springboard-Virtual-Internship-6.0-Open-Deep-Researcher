import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("Error: Missing Google API key. Please set GOOGLE_API_KEY in your .env file.")
    exit(1)
