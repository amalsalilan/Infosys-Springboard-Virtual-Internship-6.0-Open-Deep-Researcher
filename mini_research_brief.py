import os
import sys
import json
from typing import List
from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class ResearchBrief(BaseModel):
    title: str
    problem_statement: str   # <= 2 sentences
    key_questions: List[str] # 1–3 items
    method_brief: List[str]  # 2–4 items
    deliverables: List[str]  # 2–3 items

def _to_dict(obj):
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    if hasattr(obj, "dict"):
        return obj.dict()
    return json.loads(json.dumps(obj))

def main():
    # --- Read topic ---
    try:
        topic = input("Enter a research topic: ").strip()
    except EOFError:
        topic = ""

    if not topic:
        print("❌ Error: No topic provided. Please run again and enter a topic.")
        sys.exit(1)

    # --- API Key ---
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("❌ Error: GOOGLE_API_KEY not set. Please add it to a .env file or environment variable.")
        sys.exit(1)

    # --- Model ---
    try:
        model = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0,
            max_retries=2,
            google_api_key=api_key,
        )
    except Exception as e:
        print(f"❌ Error initializing model: {e}")
        sys.exit(1)

    # --- Parser & Prompt ---
    parser = PydanticOutputParser(pydantic_object=ResearchBrief)
    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a research assistant. Create a concise research brief ONLY as valid JSON "
                "that exactly matches the provided schema. No code fences, no extra text."
            ),
            (
                "human",
                "Topic: {topic}\n\nReturn strictly JSON that matches this schema:\n{format_instructions}"
            ),
        ]
    )

    # --- Generate & Validate ---
    try:
        chain = prompt | model | parser
        result: ResearchBrief = chain.invoke({
            "topic": topic,
            "format_instructions": parser.get_format_instructions()
        })
    except ValidationError as ve:
        print("❌ JSON validation failed.")
        print(str(ve))
        sys.exit(1)
    except Exception as e:
        print("❌ Error during generation:", e)
        sys.exit(1)

    # --- Output ---
    as_json = _to_dict(result)
    print("\n✅ JSON Output:")
    print(json.dumps(as_json, indent=2, ensure_ascii=False))

    print("\n📝 Markdown Preview:")
    print(f"# {result.title}\n")
    print(f"**Problem Statement:** {result.problem_statement}\n")
    print("**Key Questions:**")
    for q in result.key_questions:
        print(f"- {q}")
    print("\n**Method Brief:**")
    for m in result.method_brief:
        print(f"- {m}")
    print("\n**Deliverables:**")
    for d in result.deliverables:
        print(f"- {d}")

if __name__ == "__main__":
    main()
