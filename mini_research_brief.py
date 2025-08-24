
from dotenv import load_dotenv
import os
import json
from typing import List
from pydantic import BaseModel, ValidationError
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate

load_dotenv()

# Define schema
class ResearchBrief(BaseModel):
    title: str
    problem_statement: str   # <= 2 sentences
    key_questions: List[str] # 1–3 items
    method_brief: List[str]  # 2–4 items
    deliverables: List[str]  # 2–3 items

def main():
    # Check for API key
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        print("ERROR: GOOGLE_API_KEY not set. Please export it before running.")
        return

    # Get topic from user
    topic = input("Enter research topic: ").strip()
    if not topic:
        print("ERROR: No topic provided.")
        return

    # Initialize model
    llm = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash-latest",
        temperature=0,
        max_output_tokens=512,
        google_api_key=api_key
    )

    # Parser
    parser = PydanticOutputParser(pydantic_object=ResearchBrief)

    # Prompt
    prompt = PromptTemplate(
        template=(
            "You are a research assistant. Generate a concise research brief for the topic: {topic}.\n\n"
            "Return JSON strictly matching this schema:\n{format_instructions}"
        ),
        input_variables=["topic"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    try:
        _input = prompt.format_prompt(topic=topic)
        output = llm.invoke(_input.to_messages())

        # Parse output
        brief = parser.parse(output.content)

        # Print JSON
        print("\nStructured JSON Output:\n")
        print(json.dumps(brief.model_dump(), indent=2))

        # Markdown preview
        print("\nMarkdown Preview:\n")
        print(f"# {brief.title}\n")
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

    except ValidationError as e:
        print("ERROR: Invalid response format.")
        print(e)
    except Exception as e:
        print("ERROR:", str(e))

if __name__ == "__main__":
    main()
