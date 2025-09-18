# main.py

import json
import operator
from typing_extensions import TypedDict, Annotated, List, Sequence, Literal
from pydantic import BaseModel, Field

from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.markdown import Markdown

from langchain_core.messages import (
    BaseMessage, HumanMessage, SystemMessage, ToolMessage, filter_messages
)
from langchain_core.tools import tool, InjectedToolArg
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END

# Import configs & prompts
from configurations import (
    model, summarization_model, compress_model,
    tavily_client, get_today_str
)
from prompts import (
    research_agent_prompt, summarize_webpage_prompt,
    compress_research_system_prompt, compress_research_human_message
)

console = Console()

# ========= DISPLAY HELPERS =========
def show_prompt(prompt_text: str, title: str = "Prompt", border_style: str = "blue"):
    formatted_text = Text(prompt_text)
    formatted_text.highlight_regex(r'<[^>]+>', style="bold blue")
    formatted_text.highlight_regex(r'##[^#\n]+', style="bold magenta")
    formatted_text.highlight_regex(r'###[^#\n]+', style="bold cyan")
    console.print(Panel(formatted_text, title=f"[bold green]{title}[/bold green]", border_style=border_style, padding=(1, 2)))


# ========= STATE DEFINITIONS =========
class ResearcherState(TypedDict):
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]
    tool_call_iterations: int
    research_topic: str
    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]

class ResearcherOutputState(TypedDict):
    compressed_research: str
    raw_notes: Annotated[List[str], operator.add]
    researcher_messages: Annotated[Sequence[BaseMessage], add_messages]


# ========= SCHEMAS =========
class ClarifyWithUser(BaseModel):
    need_clarification: bool = Field(description="Whether user needs clarifying question")
    question: str = Field(description="Clarifying question")
    verification: str = Field(description="Verification message after user response")

class ResearchQuestion(BaseModel):
    research_brief: str = Field(description="Guiding research question")

class Summary(BaseModel):
    summary: str = Field(description="Concise summary of webpage content")
    key_excerpts: str = Field(description="Important quotes and excerpts")


# ========= SEARCH & SUMMARIZATION FUNCTIONS =========
def tavily_search_multiple(search_queries: List[str], max_results: int = 3, topic: Literal["general", "news", "finance"] = "general", include_raw_content: bool = True) -> List[dict]:
    search_docs = []
    for query in search_queries:
        result = tavily_client.search(query, max_results=max_results, include_raw_content=include_raw_content, topic=topic)
        search_docs.append(result)
    return search_docs

def summarize_webpage_content(webpage_content: str) -> str:
    try:
        structured_model = summarization_model.with_structured_output(Summary)
        summary = structured_model.invoke([
            HumanMessage(content=summarize_webpage_prompt.format(webpage_content=webpage_content, date=get_today_str()))
        ])
        return f"<summary>\n{summary.summary}\n</summary>\n\n<key_excerpts>\n{summary.key_excerpts}\n</key_excerpts>"
    except Exception as e:
        print(f"Failed to summarize webpage: {str(e)}")
        return webpage_content[:1000] + "..." if len(webpage_content) > 1000 else webpage_content

def deduplicate_search_results(search_results: List[dict]) -> dict:
    unique_results = {}
    for response in search_results:
        for result in response['results']:
            if result['url'] not in unique_results:
                unique_results[result['url']] = result
    return unique_results

def process_search_results(unique_results: dict) -> dict:
    summarized_results = {}
    for url, result in unique_results.items():
        content = result['content'] if not result.get("raw_content") else summarize_webpage_content(result['raw_content'])
        summarized_results[url] = {'title': result['title'], 'content': content}
    return summarized_results

def format_search_output(summarized_results: dict) -> str:
    if not summarized_results:
        return "No valid search results found."
    output = "Search results:\n\n"
    for i, (url, result) in enumerate(summarized_results.items(), 1):
        output += f"\n--- SOURCE {i}: {result['title']} ---\nURL: {url}\n\nSUMMARY:\n{result['content']}\n\n{'-'*80}\n"
    return output


# ========= TOOLS =========
@tool(parse_docstring=True)
def tavily_search(query: str, max_results: Annotated[int, InjectedToolArg] = 3, topic: Annotated[Literal["general", "news", "finance"], InjectedToolArg] = "general") -> str:
    search_results = tavily_search_multiple([query], max_results=max_results, topic=topic, include_raw_content=True)
    unique_results = deduplicate_search_results(search_results)
    summarized_results = process_search_results(unique_results)
    return format_search_output(summarized_results)

@tool(parse_docstring=True)
def think_tool(reflection: str) -> str:
    return f"Reflection recorded: {reflection}"


# ========= AGENT LOGIC =========
tools = [tavily_search, think_tool]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

def llm_call(state: ResearcherState):
    return {"researcher_messages": [model_with_tools.invoke([SystemMessage(content=research_agent_prompt)] + state["researcher_messages"])]}

def tool_node(state: ResearcherState):
    tool_calls = state["researcher_messages"][-1].tool_calls
    observations, outputs = [], []
    for tool_call in tool_calls:
        tool = tools_by_name[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        outputs.append(ToolMessage(content=result, name=tool_call["name"], tool_call_id=tool_call["id"]))
    return {"researcher_messages": outputs}

def compress_research(state: ResearcherState) -> dict:
    system_message = compress_research_system_prompt.format(date=get_today_str())
    messages = [SystemMessage(content=system_message)] + state.get("researcher_messages", []) + [HumanMessage(content=compress_research_human_message)]
    response = compress_model.invoke(messages)
    raw_notes = [str(m.content) for m in filter_messages(state["researcher_messages"], include_types=["tool", "ai"])]
    return {"compressed_research": str(response.content), "raw_notes": ["\n".join(raw_notes)]}

def should_continue(state: ResearcherState) -> Literal["tool_node", "compress_research"]:
    return "tool_node" if state["researcher_messages"][-1].tool_calls else "compress_research"


# ========= GRAPH =========
agent_builder = StateGraph(ResearcherState, output=ResearcherOutputState)
agent_builder.add_node("llm_call", llm_call)
agent_builder.add_node("tool_node", tool_node)
agent_builder.add_node("compress_research", compress_research)
agent_builder.add_edge(START, "llm_call")
agent_builder.add_conditional_edges("llm_call", should_continue, {"tool_node": "tool_node", "compress_research": "compress_research"})
agent_builder.add_edge("tool_node", "llm_call")
agent_builder.add_edge("compress_research", END)
researcher_agent = agent_builder.compile()


# ========= RUN EXAMPLE =========
if _name_ == "_main_":
    show_prompt(research_agent_prompt, "Research Agent Instruction")

    research_brief = """I want to identify and evaluate the best places to visit in India for tourism in 2025.
    My research should focus on analyzing and comparing popular destinations across India,
    considering factors like cultural significance, natural beauty, historical importance,
    accessibility, and visitor experiences."""
    
    result = researcher_agent.invoke({
        "researcher_messages": [HumanMessage(content=research_brief)],
        "tool_call_iterations": 0,
        "research_topic": "Best places to visit in India 2025",
        "compressed_research": "",
        "raw_notes": []
    })

    console.print(Markdown(result["compressed_research"]))