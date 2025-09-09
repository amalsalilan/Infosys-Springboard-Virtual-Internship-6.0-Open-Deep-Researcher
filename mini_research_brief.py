# mini_research_brief.py

# mini_research_brief.py

import os
import json
from typing import List
from pydantic import BaseModel, ValidationError
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from datetime import datetime   # ✅ Added for present time

# Load environment variables
load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("Missing Google API key. Please set it in a .env file.")


class ResearchBrief(BaseModel):
    title: str
    problem_statement: str   # <= 2 sentences
    key_questions: List[str] # 1–3 items
    method_brief: List[str]  # 2–4 items
    deliverables: List[str]  # 2–3 items


# Initialize model
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0,
    max_retries=2,
    google_api_key=api_key
)

# Output parser
parser = PydanticOutputParser(pydantic_object=ResearchBrief)

# Prompt template
prompt = PromptTemplate(
    template=(
        "You are a research assistant. Generate a structured research brief for the topic:\n\n"
        "Topic: {topic}\n\n"
        "Follow this schema strictly:\n{format_instructions}"
    ),
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

def generate_research_brief(topic: str):
    try:
        _input = prompt.format(topic=topic)
        output = llm.invoke(_input)
        brief = parser.parse(output.content)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Print JSON
        print("\n=== JSON Output ===")
        print(json.dumps({
            "generated_at": current_time,   # ✅ Add timestamp
            **brief.model_dump()
        }, indent=2))

        # Print Markdown preview
        print("\n=== Markdown Preview ===")
        print(f"# {brief.title}\n")
        print(f"**Generated At:** {current_time}\n")  # ✅ Add timestamp in preview
        print(f"**Problem Statement:** {brief.problem_statement}\n")
        print("**Key Questions:**")
        for q in brief.key_questions:
            print(f"- {q}")
        print("\n**Method Brief:**")
        for m in brief.method_brief:
            print(f"- {m}")
        print("\n**Deliverables:**")
        for d in brief.deliverables:
            print(f"- {d}")

    except ValidationError as ve:
        print("Validation error:", ve)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    topic = input("Enter research topic: ").strip()
    if not topic:
        print("Error: No topic provided.")
    else:
        generate_research_brief(topic)
