import os
from dotenv import load_dotenv
from datetime import date
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel

# Load environment variables from .env file
load_dotenv()

# ✅ 1. API key
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise EnvironmentError("❌ Error: Missing GOOGLE_API_KEY environment variable.")

# ✅ 2. LLM initialization
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_retries=2,
    google_api_key=GOOGLE_API_KEY
)

# ✅ 3. Date
TODAY = str(date.today())

# ✅ 4. Prompt template
prompt = ChatPromptTemplate.from_template(
    """
    Today is {date}.
    Generate a research brief for the topic: {topic}.

    {format_instructions}
    """
)

# ✅ 5. Pydantic schema for parsing
class ResearchBrief(BaseModel):
    date: str
    title: str
    problem_statement: str
    key_questions: list[str]
    method_brief: list[str]
    deliverables: list[str]

parser = PydanticOutputParser(pydantic_object=ResearchBrief)
