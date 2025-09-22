import operator
from typing_extensions import Optional, Annotated, Sequence
from langgraph.graph import MessagesState
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage
from pydantic import BaseModel, Field

class AgentInputState(MessagesState):
    """Input state containing only user messages"""
    pass

class AgentState(MessagesState):
    """Main state for multiagent research system"""
    research_brief: Optional[str]
    supervisor_messages: Annotated[Sequence[BaseMessage], add_messages]
    raw_notes: Annotated[list[str], operator.add] = []
    notes: Annotated[list[str], operator.add] = []
    final_report: str

class ClarifyWithUser(BaseModel):
    need_clarification: bool = Field(...)
    question: str = Field(...)
    verification: str = Field(...)

class ResearchQuestion(BaseModel):
    research_brief: str = Field(...)
