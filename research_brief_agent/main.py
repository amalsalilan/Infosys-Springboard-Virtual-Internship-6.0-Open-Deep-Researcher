# main.py
import sys
import json
from pydantic import ValidationError
from agent import build_chain
from tools import get_today_date_ist
from models import ResearchPlan
from typing import Any

def markdown_preview(plan: ResearchPlan) -> str:
    # you can copy the pretty renderer you already had
    lines = [
        f"# {plan.title}",
        f"*Generated on (IST): {plan.date}*",
        "",
        f"**Objective:** {plan.objective}",
        "",
        "## Key Questions",
        *[f"- {q}" for q in plan.key_questions],
        "",
        "## Methodology",
        *[f"- {m}" for m in plan.methodology],
        "",
        "## Search Strategy",
        *[f"- {s}" for s in plan.search_strategy],
        "",
        "## Sources to Start",
        *[f"- {src}" for src in plan.sources_to_start],
        "",
        "## Milestones & Timeline",
        *[f"- **{ms.name}** — {ms.due_date}" + (f": {ms.description}" if ms.description else "") for ms in plan.milestones_timeline],
        "",
        "## Risks & Mitigations",
        *[f"- **Risk:** {r.risk}  \n  **Mitigation:** {r.mitigation}" for r in plan.risks_mitigations],
        "",
        "## Deliverables",
        *[f"- {d}" for d in plan.deliverables],
    ]
    return "\n".join(lines)

def main():
    topic = input("Enter your research topic: ").strip()
    if not topic:
        print("Error: You must provide a non-empty topic.", file=sys.stderr)
        sys.exit(1)

    today_ist = get_today_date_ist()

    try:
        chain = build_chain()
    except Exception as e:
        print(f"Setup error: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        plan: ResearchPlan = chain.invoke({"topic": topic, "date": today_ist})
    except ValidationError as ve:
        print("Validation error from model output:", file=sys.stderr)
        print(ve, file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print("Model call failed:", file=sys.stderr)
        print(e, file=sys.stderr)
        sys.exit(1)

    print("\n=== JSON ===")
    print(json.dumps(plan.model_dump(), indent=2, ensure_ascii=False))
    print("\n=== Markdown Preview ===")
    print(markdown_preview(plan))

if __name__ == "__main__":
    main()
