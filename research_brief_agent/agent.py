# agent.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from models import ResearchPlan
from prompts import SYSTEM_PROMPT, HUMAN_PROMPT
from config import get_env

def _make_structured(model_name: str, api_key: str) -> Runnable:
    llm = ChatGoogleGenerativeAI(
        model=model_name,
        temperature=0,
        max_retries=2,
        api_key=api_key,
    )
    return llm.with_structured_output(ResearchPlan)

def build_chain() -> Runnable:
    api_key = get_env("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing Google API key. Set GOOGLE_API_KEY in .env")

    primary_model = get_env("GEMINI_MODEL", "gemini-1.5-flash")
    fallback_model = get_env("GEMINI_FALLBACK_MODEL", "gemini-1.5-flash-8b")

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", HUMAN_PROMPT),
    ])

    try:
        structured = _make_structured(primary_model, api_key)
    except Exception:
        structured = _make_structured(fallback_model, api_key)

    return prompt | structured
