import json
from datetime import datetime
from pydantic import ValidationError

# Local imports
from config import llm
from models import ResearchBrief, parser, prompt


def generate_research_brief(topic: str) -> ResearchBrief:
    """Generate research brief from LLM response and validate with schema."""
    formatted_prompt = prompt.format(
        topic=topic,
        format_instructions=parser.get_format_instructions()
    )

    raw_response = llm.invoke(formatted_prompt)
    result: ResearchBrief = parser.parse(raw_response.content)

    # Add current date
    result.date = datetime.now().strftime("%Y-%m-%d")
    return result


def print_output(result: ResearchBrief):
    """Prints both JSON and Markdown preview."""
    print("\n********* JSON Output *********\n")
    print(json.dumps(result.model_dump(), indent=2))

    print("\n********* Markdown Preview *********\n")
    print(f"# {result.title}\n")
    print(f"* Date: {result.date}\n")
    print(f"* Problem Statement: {result.problem_statement}\n")

    print("------------ Key Questions ------------")
    for q in result.key_questions:
        print(f"- {q}")

    print("\n------------ Method Brief ------------")
    for m in result.method_brief:
        print(f"- {m}")

    print("\n------------ Deliverables ------------")
    for d in result.deliverables:
        print(f"- {d}")


def main():
    topic = input("Enter your research topic: ").strip()
    if not topic:
        print("No topic provided. Please run again with a valid research topic.")
        return

    try:
        result = generate_research_brief(topic)
        print_output(result)
    except ValidationError as ve:
        print("Output validation failed:", ve)
    except Exception as e:
        print("Error generating research brief:", e)


if __name__ == "__main__":
    main()
