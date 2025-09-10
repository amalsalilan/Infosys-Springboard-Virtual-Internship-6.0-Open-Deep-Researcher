# configurations.py
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from datetime import datetime
from typing import List
from pydantic import BaseModel
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

# Load environment variables
load_dotenv()

# === API & Model Settings ===
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
MODEL_NAME = "gemini-1.5-flash-latest"
TEMPERATURE = 0
MAX_OUTPUT_TOKENS = 512
MAX_RETRIES = 2

# Initialize model
llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    temperature=TEMPERATURE,
    max_output_tokens=MAX_OUTPUT_TOKENS,
    google_api_key=GOOGLE_API_KEY
)

# === Date Settings ===
TODAY = datetime.now().strftime("%Y-%m-%d")

# === Schema ===

class ResearchBrief(BaseModel):
    date: str
    title: str
    problem_statement: str   # <= 2 sentences
    key_questions: List[str] # 1–3 items
    method_brief: List[str]  # 2–4 items
    deliverables: List[str]  # 2–3 items

# Parser
parser = PydanticOutputParser(pydantic_object=ResearchBrief)

# Prompt
prompt = PromptTemplate(
    template=(
        "You are a research assistant. Generate a concise research brief for the topic: {topic}.\n"
        "Today’s date is {date}. Use the most recent information available up to this date.\n\n"
        "Return JSON strictly matching this schema:\n{format_instructions}"
    ),
    input_variables=["topic", "date"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)