import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()

# Initialize the model
model = init_chat_model(
    "gemini-2.5-pro",
    model_provider="google_genai",
    temperature=0
)
