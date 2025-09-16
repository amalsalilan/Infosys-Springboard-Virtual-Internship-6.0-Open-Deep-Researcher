import os
import json
from typing import List
from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from datetime import date as dt
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError("Google API key is missing. Please set it in .env")

# Define Pydantic model (schema)
class ResearchBrief(BaseModel):
    title: str
    problem_statement: str   # <= 2 sentences
    key_questions: List[str] # 1–3 items
    method_brief: List[str]  # 2–4 items
    deliverables: List[str]  # 2–3 items
    date: str = dt.today().isoformat()

# Initialize Gemini model
model = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    google_api_key=api_key,
    temperature=0
)

# Initialize parser
parser = PydanticOutputParser(pydantic_object=ResearchBrief)

# Build prompt template
prompt_template = PromptTemplate(
    template="""
    You are a research assistant. Generate a concise research brief for the topic: "{topic}".
    
    The output must strictly follow this format:
    {format_instructions}
    
    Guidelines:
    - Make the brief structured and practical.
    - Keep it concise.
    """,
    input_variables=["topic"],
    partial_variables={"format_instructions": parser.get_format_instructions()},
)

# Ensure folders exist
os.makedirs("samples/input", exist_ok=True)
os.makedirs("samples/output", exist_ok=True)
os.makedirs("samples/markdownPreview", exist_ok=True)

def generate_research_brief(topic: str) -> ResearchBrief:
    if not topic.strip():
        raise ValueError("Research topic cannot be empty.")

    # Create prompt with topic
    prompt = prompt_template.format(topic=topic)

    try:
        response = model.invoke(prompt)
        return parser.parse(response.content)

    except ValidationError as ve:
        print("Error: Model output did not match schema:", ve)
        raise
    except Exception as e:
        print("Error generating research brief:", e)
        raise

def save_files(topic: str, brief: ResearchBrief, idx: int):
    # Save input
    with open(f"samples/input/sample{idx}.txt", "w") as f:
        f.write(topic)

    # Save JSON output
    with open(f"samples/output/sample{idx}.json", "w") as f:
        f.write(brief.model_dump_json(indent=2))

    # Save Markdown preview
    md_content = f"# {brief.title}\n"
    md_content += f"*Date: {brief.date}*\n\n"
    md_content += f"**Problem Statement:** {brief.problem_statement}\n\n"
    md_content += "**Key Questions:**\n"
    for q in brief.key_questions:
        md_content += f"- {q}\n"
    md_content += "\n**Methods:**\n"
    for m in brief.method_brief:
        md_content += f"- {m}\n"
    md_content += "\n**Deliverables:**\n"
    for d in brief.deliverables:
        md_content += f"- {d}\n"

    with open(f"samples/markdownPreview/sample{idx}.md", "w") as f:
        f.write(md_content)

def main():
    topic = input("Enter research topic: ")
    try:
        brief = generate_research_brief(topic)
        print("\nJSON Output:\n", brief.model_dump_json(indent=2))
        print("\nMarkdown Preview:\n")
        print(f"# {brief.title}")
        print(f"*Date: {brief.date}*\n")
        print(f"**Problem Statement:** {brief.problem_statement}\n")
        print("**Key Questions:**")
        for q in brief.key_questions:
            print(f"- {q}")
        print("\n**Methods:**")
        for m in brief.method_brief:
            print(f"- {m}")
        print("\n**Deliverables:**")
        for d in brief.deliverables:
            print(f"- {d}")

        # Save files
        existing = len(os.listdir("samples/input")) + 1
        save_files(topic, brief, existing)

    except Exception:
        print("Failed to generate research brief.")

if __name__ == "__main__":
    main()

