from workflow import scope_research
from langchain_core.messages import HumanMessage
from utils import format_messages
from rich.console import Console
from rich.markdown import Markdown

console = Console()

if __name__ == "__main__":
    thread = {"configurable": {"thread_id": "1"}}
    
    # Take user query
    user_input = input("Enter your query: ")
    
    # Run the workflow
    result = scope_research.invoke({"messages": [HumanMessage(content=user_input)]}, config=thread)
    
    # Show intermediate messages
    format_messages(result['messages'])
    
    
    followup = scope_research.invoke({"messages": [HumanMessage(content="what was the topic we were talking about ?")]}, config=thread)
    format_messages(followup['messages'])
    
    # --- Print the final research brief nicely ---
    if "research_brief" in result:
        console.print("\n[bold green]Generated Research Brief:[/bold green]\n")
        console.print(Markdown(result["research_brief"]))
