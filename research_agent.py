import os
import json
from datetime import datetime
from pydantic import ValidationError
from langgraph.graph import StateGraph

# Local imports
from configuration import llm
from models import ResearchBrief, parser
from prompts import prompt
from state import ResearchState

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
    print("\n*** JSON Output ***\n")
    print(json.dumps(result.model_dump(), indent=2))

    print("\n*** Markdown Preview ***\n")
    print(f"# {result.title}\n")
    print(f"* Date: {result.date}\n")
    print(f"* Problem Statement: {result.problem_statement}\n")

    print("--- Key Questions ---")
    for q in result.key_questions:
        print(f"- {q}")

    print("\n--- Method Brief ---")
    for m in result.method_brief:
        print(f"- {m}")

    print("\n--- Deliverables ---")
    for d in result.deliverables:
        print(f"- {d}")

def export_research_brief(result):
    """Export research brief to JSON + Markdown files in sample/ folder with numbered filenames."""
    os.makedirs("sample", exist_ok=True)

    # Find next available number
    existing_numbers = []
    for fname in os.listdir("sample"):
        match = None
        if fname.startswith("sample") and fname.endswith((".json", ".md")):
            try:
                num = int(''.join(filter(str.isdigit, fname)))
                existing_numbers.append(num)
            except:
                continue
    next_number = max(existing_numbers, default=0) + 1

    base_filename = f"sample{next_number}"
    json_path = os.path.join("sample", f"{base_filename}.json")
    md_path = os.path.join("sample", f"{base_filename}.md")

    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(result.model_dump(), f, indent=2)

    # Save Markdown
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(f"# {result.title}\n\n")
        f.write(f"* Date: {result.date}\n")
        f.write(f"* Problem Statement: {result.problem_statement}\n\n")
        f.write("## Key Questions\n")
        for q in result.key_questions:
            f.write(f"- {q}\n")
        f.write("\n## Method Brief\n")
        for m in result.method_brief:
            f.write(f"- {m}\n")
        f.write("\n## Deliverables\n")
        for d in result.deliverables:
            f.write(f"- {d}\n")

    print("\nExported files in - sample/:")
    print("- sample/.json")
    print("- sample/.md")
    
# ----------------------------------------------------- #
#                   Workflow Nodes                      #
# ----------------------------------------------------- #

def generate_node(state: ResearchState) -> ResearchState:
    try:
        result = generate_research_brief(state["topic"])
        return {"research_brief": result.model_dump()}
    except ValidationError as ve:
        return {"errors": [f"Validation failed: {ve}"]}


def refine_node(state: ResearchState) -> ResearchState:
    return state


def export_node(state: ResearchState) -> ResearchState:
    if not state.get("research_brief"):
        return {"errors": ["No research brief to export."]}

    brief = ResearchBrief(**state["research_brief"])
    print_output(brief)
    export_research_brief(brief)
    return state

# ----------------------------------------------------- #
#                     Workflow                          #
# ----------------------------------------------------- #

def build_workflow():
    graph = StateGraph(ResearchState)

    graph.add_node("generate", generate_node)
    graph.add_node("refine", refine_node)
    graph.add_node("export", export_node)

    graph.add_edge("generate", "refine")
    graph.add_edge("refine", "export")

    graph.set_entry_point("generate")
    return graph.compile()


def main():
    topic = input("Enter your research topic: ").strip()
    if not topic:
        print("No topic provided. Please run again with a valid research topic.")
        return

    try:
        workflow = build_workflow()
        state = {"topic": topic}

        # Run the workflow
        final_state = workflow.invoke(state)

        # Save workflow graph
        workflow.get_graph().draw_png("workflow_graph.png")
        print("\nWorkflow graph saved as workflow_graph.png")

        if "errors" in final_state:
            print("Errors:", final_state["errors"])

    except Exception as e:
        print("Error running workflow:", e)

if __name__ == "__main__":
    main()