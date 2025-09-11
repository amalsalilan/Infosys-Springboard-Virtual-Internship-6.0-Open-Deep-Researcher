from typing import List, Optional
from typing_extensions import TypedDict

class ResearchState(TypedDict, total=False):
    topic: str
    research_brief: Optional[dict]
    errors: List[str]
    messages: List[str]  # For future chatbot extensions

# Optional reducer if you want chatbot-like memory
def add_messages(left: List[str], right: List[str]) -> List[str]:
    return left + right