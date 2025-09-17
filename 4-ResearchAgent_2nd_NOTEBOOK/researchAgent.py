# researchAgent.py
"""
Main clarify -> research pipeline.
Depends on:
 - Configurations.py (must expose `llm` and `TODAY`)
 - Prompts.py (get_research_brief_prompt)
 - models.py (ResearchBrief Pydantic model)
 - researcher_agent.py (the researcher implementation; in same folder)
"""

from typing import TypedDict, Optional
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field, ValidationError
import json
import os

from langchain_core.messages import HumanMessage, AIMessage

# your modules (ensure same directory)
from Configurations import llm, TODAY
from Prompts import get_research_brief_prompt
from models import ResearchBrief

# researcher agent we just created
from researcher_agent import researcher_agent, format_messages_for_display

# Get prompt + parser
prompt, parser = get_research_brief_prompt()

# ===== SCHEMA FOR CLARIFICATION =====
class ClarifyWithUser(BaseModel):
    need_clarification: bool = Field(description="Whether a clarification is needed")
    question: str = Field(description="A question to ask the user")
    verification: str = Field(description="Verification message to start research")

# ===== STATE =====
class ResearchState(TypedDict):
    topic: str
    date: str
    raw_output: Optional[str]
    parsed_brief: Optional[ResearchBrief]
    messages: list
    last_decision: Optional[dict]

# ===== NODES =====
def clarify_with_user(state: ResearchState) -> ResearchState:
    """Ask clarifying questions until the model says we can proceed."""
    structured = llm.with_structured_output(ClarifyWithUser)
    # Give the model a short context: the topic & date & recent conversation
    messages = [HumanMessage(content=f"Topic: {state['topic']}. Date: {state['date']}")]
    resp = structured.invoke(messages)
    # Save structured result dict
    state["last_decision"] = resp.model_dump() if hasattr(resp, "model_dump") else dict(resp)
    if resp.need_clarification:
        # ask user for input (blocking)
        print(f"\n Clarification needed: {resp.question}")
        user_ans = input("Your clarification: ").strip()
        # update messages
        return {
            "topic": user_ans,
            "messages": state.get("messages", []) + [AIMessage(content=resp.question), HumanMessage(content=user_ans)]
        }
    else:
        # no clarification
        print(f"\n {resp.verification}")
        return {
            "messages": state.get("messages", []) + [AIMessage(content=resp.verification)]
        }

def generate_brief(state: ResearchState) -> ResearchState:
    """Generate structured brief JSON from LLM using prompt + parser"""
    # Use prompt.format_prompt as your Prompts.py defined it
    _input = prompt.format_prompt(topic=state["topic"], today_date=state["date"])
    # ask Gemini to give structured ResearchBrief; use with_structured_output if available
    structured = llm.with_structured_output(ResearchBrief)
    response = structured.invoke(_input.to_messages())
    # The model may return a pydantic model-like object or simple dict; store raw dict
    raw = response.model_dump() if hasattr(response, "model_dump") else dict(response)
    state["raw_output"] = raw
    return {"raw_output": raw}

def parse_brief(state: ResearchState) -> ResearchState:
    """Parse raw output into ResearchBrief instance"""
    raw = state.get("raw_output")
    try:
        if isinstance(raw, dict):
            brief = ResearchBrief(**raw)
        else:
            # if it's a string, try parser.parse
            brief = parser.parse(raw)
        # We don't put date in model in your models, but if you have it, set; otherwise leave
        return {"parsed_brief": brief}
    except Exception as e:
        print("ERROR parsing brief:", e)
        return {"parsed_brief": None}

# router after clarify
def route_after_clarify(state: ResearchState) -> str:
    last = state.get("last_decision")
    if last and last.get("need_clarification", False):
        return "clarify_with_user"
    return "generate_brief"

# brief->scope helper
def brief_to_scope_statement(brief: ResearchBrief) -> str:
    scope = f"I want to research {brief.title}, focusing on the key questions identified."
    if brief.problem_statement:
        scope += f" Problem: {brief.problem_statement}"
    if brief.key_questions:
        scope += " Key questions: " + "; ".join(brief.key_questions) + "."
    if brief.method_brief:
        scope += " Methods to consider: " + "; ".join(brief.method_brief) + "."
    return scope

# ===== Build Graph =====
workflow = StateGraph(ResearchState)
workflow.add_node("clarify_with_user", clarify_with_user)
workflow.add_node("generate_brief", generate_brief)
workflow.add_node("parse_brief", parse_brief)
workflow.set_entry_point("clarify_with_user")
workflow.add_conditional_edges(
    "clarify_with_user",
    route_after_clarify,
    {"clarify_with_user": "clarify_with_user", "generate_brief": "generate_brief"}
)
workflow.add_edge("generate_brief", "parse_brief")
workflow.set_finish_point("parse_brief")
clarify_agent = workflow.compile()

# ===== Run script =====
if __name__ == "__main__":
    topic = input("Enter research topic: ").strip()
    # Guard VSCode accidental path paste
    if topic.endswith(".py") or "\\" in topic or "/" in topic:
        topic = ""
    if not topic:
        topic = input("Please enter a valid research topic: ").strip()

    initial_state = {
        "topic": topic,
        "date": TODAY,
        "raw_output": None,
        "parsed_brief": None,
        "messages": [],
        "last_decision": None
    }

    # Run clarify -> brief parse
    final_state = clarify_agent.invoke(initial_state)
    brief = final_state.get("parsed_brief")

    if not brief:
        print("No valid research brief produced; exiting.")
        exit(1)

    # print conversation log (if present)
    if final_state.get("messages"):
        print("\n--- Conversation Log ---\n")
        for msg in final_state["messages"]:
            role = " Human" if isinstance(msg, HumanMessage) else " AI"
            print(f"{role}: {msg.content}\n")

    # Print research brief
    print("\n--- Research Brief ---\n")
    # if your ResearchBrief has date field, use; else skip
    try:
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
    except Exception:
        print("(Could not pretty print the brief.)")

    # Convert brief → scope for the research agent
    scope_statement = brief_to_scope_statement(brief)
    print("\n--- Research Scope Statement ---\n")
    print(scope_statement + "\n")

    # ===== Run researcher agent
    print("\n Running Research Agent...\n")
    research_result = researcher_agent(scope_statement)

    print("\n--- Research Agent Output ---\n")
    print(research_result.get("compressed_research","(no report)"))

    print("\n--- Sources ---\n")
    for s in research_result.get("sources",[]):
        print(s)

