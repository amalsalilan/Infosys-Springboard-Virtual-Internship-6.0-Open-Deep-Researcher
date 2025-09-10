
# Configurations.py
import os
from dotenv import load_dotenv
from datetime import datetime
from langchain_google_genai import ChatGoogleGenerativeAI

# === Load API Key ===
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("Missing GOOGLE_API_KEY in environment variables.")

# === Initialize LLM ===
MODEL_NAME = "gemini-1.5-flash-latest"
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=0,
    max_output_tokens=512,
    google_api_key=GOOGLE_API_KEY,
)

# === Date ===
TODAY = datetime.now().strftime("%Y-%m-%d")


