from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent

from config import GOOGLE_API_KEY
from tools import get_date_today
from prompts import prompt

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    model_provider="google-genai",
    temperature=0,
    max_retries=2,
    max_tokens=None,
    timeout=None,
    api_key=GOOGLE_API_KEY
)

# Define available tools
TOOLS = [get_date_today]

# Create agent
agent = create_react_agent(
    model=model,
    tools=TOOLS,
    prompt=prompt,
)
