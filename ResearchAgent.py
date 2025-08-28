import os
from dotenv import load_dotenv
from datetime import datetime   
from langchain_google_genai import ChatGoogleGenerativeAI

from models import ResearchBrief
from prompts import get_research_brief_prompt



def get_today_date() -> str:
    """Return today's date as YYYY-MM-DD string."""
    return datetime.today().strftime("%Y-%m-%d")



def init_llm():
    load_dotenv()
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise EnvironmentError("Missing GOOGLE_API_KEY in environment variables.")

    return ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        max_retries=2,
        google_api_key=api_key,
    )


def generate_research_brief(topic: str) -> ResearchBrief:
    llm = init_llm()
    prompt, parser = get_research_brief_prompt()
    chain = prompt | llm | parser
    brief = chain.invoke({
        "topic": topic,
        "today_date": get_today_date()   
    })

    
    brief.key_questions = brief.key_questions[:3]
    brief.method_brief = brief.method_brief[:4]
    brief.deliverables = brief.deliverables[:3]

    return brief


if __name__ == "__main__":
    try:
        topic = input("Enter your research topic: ").strip()
        if not topic:
            raise ValueError("Error: No topic provided.")

        brief = generate_research_brief(topic)

        print("\n JSON Output:\n")
        print(brief.model_dump_json(indent=2))

        print("\n Markdown Preview:\n")
        print(f"# {brief.title}\n")
        print(f"**Date:** {get_today_date()}\n")  
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

    except Exception as e:
        print(f"\n Error: {e}")


