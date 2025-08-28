import os
import json
from typing import List
from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from dotenv import load_dotenv

from datetime import datetime
import pytz

# Load environment variables from .env
load_dotenv()

class ResearchPlan(BaseModel):
    title: str
    date: str
    objective: str
    key_questions: List[str]
    methodology: List[str]
    search_strategy: List[str]
    sources_to_start: List[str]
    risks_mitigations: List[str]
    deliverables: List[str]

def get_today_date():
    tz = pytz.timezone("Asia/Kolkata")
    return datetime.now(tz).strftime("%Y-%m-%d")

def main():
    # Hardcoded research topic
    topic = "what is ai"

    if not topic:
        print("Error: No topic provided.")
        return

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: Missing GOOGLE_API_KEY in environment.")
        return

    today_date = get_today_date()
    parser = PydanticOutputParser(pydantic_object=ResearchPlan)

    prompt = ChatPromptTemplate.from_messages([
        ("system", 
         "You are a research planning assistant. Generate a concise, factual, and domain-appropriate research plan in JSON only. "
         "Include these sections: Title, Date, Objective, Key Questions, Methodology, Search Strategy, Sources to Start, "
         "Milestones & Timeline (with dates), Risks & Mitigations, Deliverables. Use today's date ({today_date}). "
         "Constraints: Be strictly focused and domain-appropriate. "
         "Do NOT fabricate or hallucinate URLs, website names, academic papers, or citations. "
         "Only provide real or plausible, verified sources."),
        ("human", "Topic: {topic}\n\n{format_instructions}")
    ]).partial(format_instructions=parser.get_format_instructions(), today_date=today_date)

    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_retries=2
    )

    chain = prompt | llm | parser

    try:
        result: ResearchPlan = chain.invoke({"topic": topic})
    except ValidationError as e:
        print("Error: Model output did not match schema:\n", e)
        return
    except Exception as e:
        print("Runtime Error:", e)
        return

    print("\nResearch Plan (JSON):")
    print(json.dumps(result.dict(), indent=2))

    print("\n### Research Plan (Markdown Preview)\n")
    print(f"**Title:** {result.title}\n")
    print(f"**Date:** {result.date}\n")
    print(f"**Objective:** {result.objective}\n")
    print("**Key Questions:**")
    for q in result.key_questions:
        print(f"- {q}")
    print("\n**Methodology:**")
    for m in result.methodology:
        print(f"- {m}")
    print("\n**Search Strategy:**")
    for s in result.search_strategy:
        print(f"- {s}")
    print("\n**Sources to Start:**")
    for src in result.sources_to_start:
        print(f"- {src}")
    print("\n**Risks & Mitigations:**")
    for rm in result.risks_mitigations:
        print(f"- {rm}")
    print("\n**Deliverables:**")
    for d in result.deliverables:
        print(f"- {d}")

if __name__ == "__main__":
    main()
