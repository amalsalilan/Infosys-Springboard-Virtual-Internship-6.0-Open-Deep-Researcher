# models.py
from typing import List, Optional, Annotated
from pydantic import BaseModel, Field
from pydantic import StringConstraints

DateStr = Annotated[str, StringConstraints(pattern=r"^\d{4}-\d{2}-\d{2}$")]

class Milestone(BaseModel):
    name: str = Field(..., description="Short milestone label")
    due_date: DateStr = Field(..., description="Due date in YYYY-MM-DD (IST)")
    description: Optional[str] = Field(None, description="1 line on what will be delivered")

class RiskItem(BaseModel):
    risk: str = Field(..., description="Concise risk")
    mitigation: str = Field(..., description="Specific mitigation or control")

class ResearchPlan(BaseModel):
    title: str
    date: DateStr
    objective: str
    key_questions: List[str]
    methodology: List[str]
    search_strategy: List[str]
    sources_to_start: List[str]
    milestones_timeline: List[Milestone]
    risks_mitigations: List[RiskItem]
    deliverables: List[str]
