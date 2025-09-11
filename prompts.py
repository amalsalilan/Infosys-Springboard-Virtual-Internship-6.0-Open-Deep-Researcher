from langchain_core.prompts import ChatPromptTemplate

# Prompt template for structured research brief
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a research assistant. Generate a concise research brief."),
    ("human", "Topic: {topic}\n\n{format_instructions}")
])