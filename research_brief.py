import json
from pydantic import ValidationError


# Import configurations
from configure import (
    GOOGLE_API_KEY,
    llm,
    TODAY,
    prompt,
    parser
)

def main():
    # Check for API key
    if not GOOGLE_API_KEY:
        print("ERROR: GOOGLE_API_KEY not set. Please export it before running.")
        return

    # Get topic from user
    topic = input("Enter research topic: ").strip()
    if not topic:
        print("ERROR: No topic provided.")
        return

    try:
        _input = prompt.format_prompt(
        topic=topic,
        date=TODAY,
        format_instructions=parser.get_format_instructions()
)

        output = llm.invoke(_input.to_messages())

        # Parse output
        brief = parser.parse(output.content)

        # Ensure correct date
        brief.date = TODAY  

        # Print JSON
        print("\nStructured JSON Output:\n")
        print(json.dumps(brief.model_dump(), indent=2))

        # Markdown preview
        print("\nMarkdown Preview:\n")
        print(f"Date: {brief.date}\n")
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
