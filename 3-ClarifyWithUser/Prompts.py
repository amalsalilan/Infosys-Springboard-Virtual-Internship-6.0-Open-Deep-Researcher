#Prompts.py
from langchain.output_parsers import PydanticOutputParser
from langchain.prompts import PromptTemplate
from models import ResearchBrief


def get_research_brief_prompt():
    parser = PydanticOutputParser(pydantic_object=ResearchBrief)

    prompt = PromptTemplate(
        template=(
            "You are a research assistant.\n"
            "Today's date is {today_date}. Ensure your response reflects the most up-to-date information.\n"
            "Create a concise research brief for the topic below.\n"
            "The output MUST follow this format:\n\n"
            "{format_instructions}\n\n"
            "Rules:\n"
            "- problem_statement: maximum 2 sentences.\n"
            "- key_questions: exactly 3 items.\n"
            "- method_brief: 2 to 4 items.\n"
            "- deliverables: 2 to 3 items.\n"
            "- Output ONLY valid JSON.\n\n"
            "Topic: {topic}"
        ),
        input_variables=["topic", "today_date"],  # this includes date
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )
    return prompt, parser
