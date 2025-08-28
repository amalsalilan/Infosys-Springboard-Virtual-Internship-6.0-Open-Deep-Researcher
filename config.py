import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# Load environment variables
load_dotenv()

# API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Missing GOOGLE_API_KEY. Please set it in your environment.")

# Model configuration
MODEL_NAME = "gemini-1.5-flash"
TEMPERATURE = 0
MAX_RETRIES = 2

# Initialize LLM
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    max_retries=MAX_RETRIES,
    google_api_key=GOOGLE_API_KEY,
)