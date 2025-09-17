# researcher_agent.py
"""
Researcher agent that:
- Accepts a scope statement (string)
- Performs a small, budgeted Tavily search loop
- Deduplicates results
- Summarizes pages with Gemini (llm)
- Produces a compressed final report similar to mentor's notebook output
"""

from dotenv import load_dotenv
load_dotenv()
import os
import json
from typing import List, Dict
from tavily import TavilyClient
from langchain_core.messages import HumanMessage
from pydantic import BaseModel

# Load env
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
if not TAVILY_API_KEY:
    raise EnvironmentError("Missing TAVILY_API_KEY in environment variables. Add it to your .env")

# Basic Tavily client
tavily = TavilyClient(api_key=TAVILY_API_KEY)

# Import the llm provided by your Configurations file (Gemini wrapper).
# Your Configurations.py should expose `llm`.
from Configurations import llm

# ---------- Helpers ----------

def _shorten_query(q: str, max_chars: int = 380) -> str:
    """Make sure query is under tavily limit (400). Trim politely."""
    if len(q) <= max_chars:
        return q
    # Try to keep semantic head by truncating on sentence boundary
    truncated = q[:max_chars]
    if "." in truncated:
        truncated = truncated.rsplit(".", 1)[0]
    return truncated.strip()

def tavily_search_one(query: str, max_results: int = 3) -> Dict:
    """Run tavily.search for a single query (wrapped with error handling)."""
    q = _shorten_query(query)
    try:
        res = tavily.search(query=q, max_results=max_results, include_raw_content=True)
        return res
    except Exception as e:
        return {"error": str(e), "results": []}

def dedupe_by_url(list_of_search_responses: List[Dict]) -> Dict[str, Dict]:
    """Turn list of Tavily responses into dict keyed by URL to dedupe."""
    unique = {}
    for resp in list_of_search_responses:
        for r in resp.get("results", []):
            url = r.get("url")
            if not url:
                continue
            if url not in unique:
                unique[url] = r
    return unique

def summarize_with_llm(raw_content: str) -> str:
    """Summarize a webpage chunk using Gemini llm (keeps short)."""
    # Lightweight summarization instruction
    prompt = (
        "You are a research assistant. Summarize the following webpage content concisely, "
        "preserving key points, facts, and any important numbers/quotes. Keep output short (approx 3-6 sentences):\n\n"
        f"{raw_content[:5000]}\n\n"  # limit length so we don't exceed token limits
    )
    try:
        resp = llm.invoke([HumanMessage(content=prompt)])
        return str(resp.content).strip()
    except Exception as e:
        return f"(Summarization failed: {e})"

def format_final_report(scope_statement: str, summarized_results: Dict[str, Dict]) -> str:
    """Assemble a final report string similar to your mentor's output."""
    lines = []
    lines.append("List of Queries and Tool Calls Made\n")
    lines.append(" • queries were issued based on the scope statement and focused filters.\n")
    lines.append("\nFully Comprehensive Findings\n")
    if not summarized_results:
        lines.append("No usable search results were found. Try other queries or check API keys.\n")
        return "\n".join(lines)

    # General context
    lines.append("General findings and key themes from sources:\n")
    # Summaries
    for idx, (url, info) in enumerate(summarized_results.items(), start=1):
        lines.append(f"\n--- SOURCE {idx}: {info.get('title','(no title)')} ---")
        lines.append(f"URL: {url}")
        lines.append("\nSUMMARY:\n")
        lines.append(info.get("summary","(no summary)"))
        if info.get("key_excerpts"):
            lines.append("\nKey excerpts:")
            lines.append(info.get("key_excerpts"))
        lines.append("\n" + "-"*80)
    # Sources list
    lines.append("\nList of All Relevant Sources (with brief titles):\n")
    for i, (url,info) in enumerate(summarized_results.items(), start=1):
        title = info.get("title","(no title)")
        lines.append(f"[{i}] {title}: {url}")
    return "\n".join(lines)

# ---------- Main researcher function ----------

def researcher_agent(scope_statement: str, max_queries: int = 3, max_results_per_query: int = 3) -> Dict:
    """
    Main entrypoint called by the clarify agent.
    Returns: dict with compressed_report (string), raw_notes (list), sources (list)
    """
    # Build 3 short focused queries derived from the scope
    # We'll create simple templates so they don't exceed tavily's length.
    base = scope_statement.strip().replace("\n"," ")
    queries = [
        f"{base} key findings",
        f"{base} top sources and reviews",
        f"{base} rankings case studies"
    ][:max_queries]

    search_responses = []
    for q in queries:
        q_short = _shorten_query(q, max_chars=380)
        res = tavily_search_one(q_short, max_results=max_results_per_query)
        # If tavily returned error, include error message
        search_responses.append(res)

    # Deduplicate
    unique_results = dedupe_by_url(search_responses)

    # Summarize each page (prefer raw_content when available)
    summarized = {}
    for url, result in unique_results.items():
        title = result.get("title") or result.get("name") or url
        raw = result.get("raw_content") or result.get("content") or ""
        if raw:
            summary = summarize_with_llm(raw)
            key_excerpts = ""  # you could extract quotes; keep blank here for simplicity
        else:
            summary = summarize_with_llm(result.get("content",""))
            key_excerpts = ""
        summarized[url] = {"title": title, "summary": summary, "key_excerpts": key_excerpts}

    # Compose final report
    compressed_report = format_final_report(base, summarized)

    # Build sources list
    sources = list(summarized.keys())

    # Raw notes: combine short summaries
    raw_notes = [v['summary'] for v in summarized.values()]

    return {
        "compressed_research": compressed_report,
        "raw_notes": raw_notes,
        "sources": sources
    }

# local helper used by researchAgent.py if needed
def format_messages_for_display(messages):
    out = []
    for m in messages:
        role = "Human" if isinstance(m, HumanMessage) else "AI"
        out.append(f"{role}: {m.content}")
    return "\n".join(out)
