from typing import List
from pydantic import BaseModel
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate


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

# Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant. Generate a concise research brief."),
    ("human", "Topic: {topic}\n\n{format_instructions}")
])