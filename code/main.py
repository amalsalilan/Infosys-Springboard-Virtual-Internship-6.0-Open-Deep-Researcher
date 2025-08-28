from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from datetime import datetime

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Define the function as a LangChain tool
@tool
def get_current_datetime() -> str:
    """Returns the current date and time."""
    now = datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")

# Create LLM model with tool
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=1,
    max_output_tokens=150,
    top_p=0.9,
).bind_tools([get_current_datetime])

# Invoke LLM
response = model.invoke("What is the current date and time?")

#Checking if LLM called a tool
if response.tool_calls:
    for call in response.tool_calls:
        if call["name"] == "get_current_datetime":
            result = get_current_datetime.invoke({})
            print("Current Date & Time:", result)
else:
    print("LLM Response:", response.content)
