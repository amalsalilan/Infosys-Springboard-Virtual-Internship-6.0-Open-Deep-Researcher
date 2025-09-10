# models.py
from pydantic import BaseModel
from typing import List, Optional

class ResearchBrief(BaseModel):
    title: str
    problem_statement: str   
    key_questions: List[str] 
    method_brief: List[str] 
    deliverables: List[str]  
    date: Optional[str] = None