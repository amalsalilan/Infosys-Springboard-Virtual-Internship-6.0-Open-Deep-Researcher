from typing import List
from pydantic import BaseModel

# Schema for research brief
class ResearchBrief(BaseModel):
    title: str
    date: str
    problem_statement: str
    key_questions: List[str]
    method_brief: List[str]
    deliverables: List[str]
