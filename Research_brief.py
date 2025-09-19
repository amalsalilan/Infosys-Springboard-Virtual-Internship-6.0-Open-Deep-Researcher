import os
import json
from typing import List
from datetime import date
from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
try:
    from langchain_core.output_parsers import OutputParserException  # type: ignore
except Exception:
    class OutputParserException(Exception):  # fallback for older versions
        pass
class ResearchBrief(BaseModel):
    title: str
    problem_statement: str  
    date: str 
    key_questions: List[str] 
    method_brief: List[str]  
    deliverables: List[str]  
                    


def main():
    topic = input("Enter your research topic: ").strip()
    if not topic:
        print("Error: No topic provided. Please rerun and enter a topic.")
        return

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("Error: GOOGLE_API_KEY environment variable not set.")
        print("   Set it and rerun. Example (PowerShell):  setx GOOGLE_API_KEY \"YOUR_KEY\"")
        return
    parser = PydanticOutputParser(pydantic_object=ResearchBrief)

    prompt = PromptTemplate(
        template=(
            "You are a research assistant. Produce a concise research brief "
            "STRICTLY as JSON that validates against the schema below.\n\n"
            "Topic: {topic}\n\n"
            "- date must be today's date (YYYY-MM-DD)\n"
            "{format_instructions}\n\n"
            "Constraints:\n"
            "- problem_statement: maximum 2 sentences\n"
            "- key_questions: 1–3 items\n"
            "- method_brief: 2–4 items\n"
            "- deliverables: 2–3 items\n"
            "Only output the JSON—no commentary."
        ),
        input_variables=["topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        temperature=0,
        max_retries=2,
        google_api_key=api_key,
    )

    try:
        chain = prompt | llm | parser
        result: ResearchBrief = chain.invoke({"topic": topic})
        result.date = date.today().isoformat()
        result_dict = result.model_dump()
        result_json = json.dumps(result_dict, indent=2, ensure_ascii=False)

        print("\nJSON Output:\n")
        print(result_json)

        print("\nMarkdown Preview:\n")
        print(f"# {result.title}\n")
        print(f"**Date:** {result.date}\n")
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

    except OutputParserException as ope:
        print("Invalid JSON from model (failed to parse/validate). Try re-running or refining the topic.")
        print(f"Details: {ope}")
    except ValidationError as ve:
        print("Validation Error (JSON didn't match the schema):")
        print(ve)
    except Exception as e:
        print("Unexpected Error:", str(e))


if __name__ == "__main__":
    main()
