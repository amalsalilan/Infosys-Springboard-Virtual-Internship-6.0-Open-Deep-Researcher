# Clarify With User
from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from pydantic import ValidationError, BaseModel, Field
import json

# LangChain types
from langchain_core.messages import HumanMessage, AIMessage

# === Imports from your setup ===
from Configurations import llm, TODAY
from Prompts import get_research_brief_prompt
from models import ResearchBrief

# Get prompt + parser
prompt, parser = get_research_brief_prompt()


# === Schema for clarification ===
class ClarifyWithUser(BaseModel):
    need_clarification: bool = Field(
        description="Whether the user needs to be asked a clarifying question."
    )
    question: str = Field(
        description="A question to ask the user to clarify the report scope."
    )
    verification: str = Field(
        description="Verification message that we will start research."
    )


# === Define State ===
class ResearchState(TypedDict):
    topic: str
    date: str
    raw_output: Optional[str]
    parsed_brief: Optional[ResearchBrief]
    messages: list  # conversation history
    last_decision: Optional[dict]  # store clarify decision


# === Nodes ===
def clarify_with_user(state: ResearchState) -> ResearchState:
    """Node 0: Ask clarifying questions if needed."""

    structured_llm = llm.with_structured_output(ClarifyWithUser)

    # Build input (using just topic + date for now)
    response = structured_llm.invoke(
        [HumanMessage(content=f"Topic: {state['topic']}, Date: {state['date']}")]
    )

    # Save decision so router can read it
    state["last_decision"] = response.model_dump()

    if response.need_clarification:
        print(f"\n Clarification needed: {response.question}")
        user_answer = input("Your clarification: ").strip()

        return {
            "topic": user_answer,
            "messages": state.get("messages", [])
            + [AIMessage(content=response.question), HumanMessage(content=user_answer)],
        }
    else:
        print(f"\n {response.verification}")
        return {
            "messages": state.get("messages", [])
            + [AIMessage(content=response.verification)],
        }


def generate_brief(state: ResearchState) -> ResearchState:
    """Node 1: Generate raw research brief text from LLM."""
    _input = prompt.format_prompt(topic=state["topic"], today_date=state["date"])
    output = llm.invoke(_input.to_messages())
    return {"raw_output": output.content}


def parse_brief(state: ResearchState) -> ResearchState:
    """Node 2: Parse the raw output into ResearchBrief model."""
    try:
        brief = parser.parse(state["raw_output"])
        brief.date = state["date"]  # overwrite date with today
        return {"parsed_brief": brief}
    except ValidationError as e:
        print("ERROR: Invalid response format.")
        print(e)
        return {"parsed_brief": None}


# === Router ===
def route_after_clarify(state: ResearchState) -> str:
    """Decide next step after clarification"""
    last_msg = state.get("last_decision")
    if last_msg and last_msg.get("need_clarification", False):
        return "clarify_with_user"
    return "generate_brief"


# === Helper: Convert brief → narrative statement ===
def brief_to_scope_statement(brief: ResearchBrief) -> str:
    """Convert structured research brief into a natural language research scope statement."""
    
    # Start with title
    scope = f"I want to research {brief.title}, focusing on the key questions identified. "

    # Add problem statement context
    if brief.problem_statement:
        scope += f"The problem we are addressing is: {brief.problem_statement} "

    # Add key questions in a natural way
    if brief.key_questions:
        scope += "The research will specifically look into: "
        scope += "; ".join(brief.key_questions) + ". "

    # Add methods as hints
    if brief.method_brief:
        scope += "The methods to be considered may include: "
        scope += "; ".join(brief.method_brief) + ". "

    # Deliverables hint (optional, only if exists)
    if brief.deliverables:
        scope += "Expected outcomes include: "
        scope += "; ".join(brief.deliverables) + "."

    return scope

# === Build Graph ===
workflow = StateGraph(ResearchState)

workflow.add_node("clarify_with_user", clarify_with_user)
workflow.add_node("generate_brief", generate_brief)
workflow.add_node("parse_brief", parse_brief)

workflow.set_entry_point("clarify_with_user")

# Conditional branching
workflow.add_conditional_edges(
    "clarify_with_user",
    route_after_clarify,
    {
        "clarify_with_user": "clarify_with_user",
        "generate_brief": "generate_brief",
    },
)

workflow.add_edge("generate_brief", "parse_brief")
workflow.set_finish_point("parse_brief")

graph = workflow.compile()


# === Run ===
if __name__ == "__main__":
    topic = input("Enter research topic: ").strip()

    # VS Code sometimes sends the file path — to filter it out
    if topic.endswith(".py") or "\\" in topic or "/" in topic:
        topic = ""

    if not topic:
        topic = input("Please enter a valid research topic: ").strip()

    # Initial state
    initial_state = {
        "topic": topic,
        "date": TODAY,
        "raw_output": None,
        "parsed_brief": None,
        "messages": [],
        "last_decision": None,
    }

    # Execute graph
    final_state = graph.invoke(initial_state)

    # Get result
    brief = final_state["parsed_brief"]

    if brief:
        print("\n--- Conversation Log ---\n")
        for msg in final_state["messages"]:
            role = " Human" if isinstance(msg, HumanMessage) else " AI"
            print(f"{role}: {msg.content}\n")

        print("\n Research Brief (Markdown Style):\n")
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

        # === NEW: Scope Statement for Next Agent ===
        print("\n Research Scope Statement :\n")
        print(brief_to_scope_statement(brief))

    # === Visualize Graph ===
    try:
        print("\n--- Workflow Graph ---")
        print(graph.get_graph().draw_ascii())
    except Exception as e:
        print("Visualization error:", e)

