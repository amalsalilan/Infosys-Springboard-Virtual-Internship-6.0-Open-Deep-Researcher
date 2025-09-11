from typing import List
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser

# Schema
class ResearchBrief(BaseModel):
    date: str
    title: str
    problem_statement: str
    key_questions: List[str]
    method_brief: List[str]
    deliverables: List[str]


# Parser
parser = PydanticOutputParser(pydantic_object=ResearchBrief)