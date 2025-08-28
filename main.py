import os
import json
from pydantic import ValidationError

from agent import agent
from models import ResearchBrief
from tools import extract_json

def main():
    print(" Mini Research Brief Generator")
    topic = input("Enter your research topic: ").strip()

    if not topic:
        print("Error: Empty topic provided. Please enter a valid research topic.")
        return

    try:
        # Ask the agent
        result = agent.invoke({"messages": [("user", f"Create a research brief for: {topic}")]}).get("messages", [])
        final_text = ""
        if result:
            last_msg = result[-1]
            final_text = getattr(last_msg, "content", "") or str(last_msg)

        # Extract & validate JSON
        clean_json = extract_json(final_text)
        data = json.loads(clean_json)
        brief = ResearchBrief(**data)


        # Save to file
        os.makedirs("samples", exist_ok=True)
        file_safe_title = topic.replace(" ", "_").lower()
        output_path = f"samples/{file_safe_title}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(brief.dict(), f, indent=2, ensure_ascii=False)

        print(f"\nJSON output saved to {output_path}")

    except json.JSONDecodeError:
        print("Error: Model did not return valid JSON.")
        print("Raw output was:\n", final_text)
    except ValidationError as ve:
        print("Error: JSON did not match schema.")
        print(ve)
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
