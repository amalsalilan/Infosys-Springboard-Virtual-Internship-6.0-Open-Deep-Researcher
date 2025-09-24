import os
import asyncio
import json
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated, Optional, Dict, Any
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import operator
import logging

# Configuration
FILES_DIRECTORY = r"C:\Users\swaroopa\PycharmProjects\MCP"

console = Console()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Enhanced prompts with better context
def get_research_prompt(question: str, context: Dict[str, Any]) -> str:
    """Generate a research prompt with enhanced context"""
    base_prompt = f"""You are analyzing files to answer this specific question: "{question}"

CONTEXT:
- Directory listed: {context.get('directory_listed', False)}
- Files already read: {context.get('files_read', 0)}
- Iteration: {context.get('iteration', 0)}
- Previous findings: {context.get('findings', 'None yet')}

Use the available tools strategically:
1. If directory not listed: Start with list_directory to see available files
2. If files not yet read: Use read_text_file on files most likely to contain relevant information
3. Consider file names, extensions, and sizes when choosing which files to read
4. Focus on extracting information that directly relates to: "{question}"

STOPPING CRITERIA:
- Stop calling tools after reading 2-3 relevant files AND gathering sufficient information
- If you have enough information to answer the question, provide your findings instead of calling more tools

Available tools: list_directory, read_text_file, search_files (if you need to find specific content)"""

    return base_prompt


def get_summary_prompt(question: str, files_analyzed: List[str]) -> str:
    """Generate a summary prompt with file context"""
    return f"""Based on your analysis of the following files: {', '.join(files_analyzed)}

Provide a comprehensive answer to this question: "{question}"

Structure your response as:
1. **Direct Answer**: Clear, concise answer to the question
2. **Supporting Evidence**: Key information from the files that supports your answer
3. **Source Files**: Which specific files contained the relevant information
4. **Confidence Level**: How confident you are in your answer (High/Medium/Low)
5. **Limitations**: Any gaps in the available data or areas where more information might be helpful

Be specific and cite which files contained which pieces of information."""


# Enhanced state schema
class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    iteration: int
    directory_listed: bool
    files_read: int
    should_continue: bool
    analysis_complete: bool
    question: str
    files_analyzed: Annotated[List[str], operator.add]  # Track which files were read
    findings: str  # Track cumulative findings
    error_count: int  # Track errors
    max_iterations: int  # Configurable max iterations


def validate_directory():
    """Enhanced directory validation with more detailed info"""
    files_path = Path(FILES_DIRECTORY)
    if not files_path.exists() or not files_path.is_dir():
        console.print(f"[red]Invalid directory: {files_path}[/red]")
        return None

    files = [f for f in files_path.iterdir() if f.is_file()]

    # Create a nice table of files
    table = Table(title=f"Files in {files_path}")
    table.add_column("Filename", style="cyan")
    table.add_column("Size", style="magenta")
    table.add_column("Extension", style="green")

    for file in files:
        size = file.stat().st_size
        size_str = f"{size} bytes" if size < 1024 else f"{size / 1024:.1f} KB"
        table.add_row(file.name, size_str, file.suffix or "No extension")

    console.print(table)
    return files_path


# Enhanced MCP Client with error handling
_client = None


async def get_mcp_client():
    """Get MCP client with better error handling"""
    global _client
    if _client is None:
        files_path = validate_directory()
        if not files_path:
            raise Exception("Cannot access directory")

        mcp_config = {
            "filesystem": {
                "command": "npx",
                "args": ["-y", "@modelcontextprotocol/server-filesystem", str(files_path.absolute())],
                "transport": "stdio"
            }
        }

        with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=console,
        ) as progress:
            task = progress.add_task("Connecting to MCP server...", total=None)
            _client = MultiServerMCPClient(mcp_config)
            await asyncio.sleep(2)
            progress.update(task, description="Getting available tools...")

            tools = await _client.get_tools()
            progress.update(task, description=f"Connected! {len(tools)} tools available")

        console.print(f"[green]MCP Client ready with {len(tools)} tools[/green]")
    return _client


# Enhanced LLM setup with better error handling
def setup_llm():
    """Setup LLM with enhanced configuration"""
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print("[red]Warning: GOOGLE_API_KEY not found in environment variables[/red]")
        # Fallback to hardcoded key (not recommended for production)
        api_key = "AIzaSyDkN6qhf5i2-nVZf6f_dk5f0WHSzyr2-mI"

    rate_limiter = InMemoryRateLimiter(
        requests_per_second=0.1,  # Slightly more conservative
        check_every_n_seconds=1,
        max_bucket_size=2
    )

    return init_chat_model(
        "gemini-2.0-flash",
        model_provider="google_genai",
        api_key=api_key,
        temperature=0.1,
        rate_limiter=rate_limiter
    )


model = setup_llm()


def analyze_state_from_messages(messages):
    """Enhanced state analysis with more details"""
    directory_listed = False
    files_read = 0
    files_analyzed = []

    for msg in messages:
        if isinstance(msg, ToolMessage):
            if msg.name == "list_directory":
                directory_listed = True
            elif msg.name in ["read_file", "read_text_file"]:
                files_read += 1
                # Try to extract filename from tool call context
                # This is a simplified approach - you might need to enhance this
                if hasattr(msg, 'content') and msg.content:
                    # Extract filename if possible from content or context
                    content_preview = str(msg.content)[:100]
                    files_analyzed.append(f"File_{files_read}")

    return directory_listed, files_read, files_analyzed


# Enhanced LangGraph node functions
async def research_step(state: AgentState) -> AgentState:
    """Enhanced research step with better state tracking"""
    try:
        console.print(f"[blue]Research Step {state['iteration']} - Question: {state['question'][:50]}...[/blue]")

        # Check termination conditions
        if state['iteration'] >= state.get('max_iterations', 5):
            console.print("[yellow]Maximum iterations reached[/yellow]")
            return {
                **state,
                "should_continue": False,
                "analysis_complete": True
            }

        # Enhanced state analysis
        directory_listed, files_read, files_analyzed = analyze_state_from_messages(state['messages'])

        # More nuanced stopping criteria
        sufficient_analysis = (
                directory_listed and
                files_read >= 2 and
                state['iteration'] >= 2
        )

        if sufficient_analysis:
            console.print("[yellow]Sufficient analysis completed - moving to summary[/yellow]")
            return {
                **state,
                "should_continue": False,
                "analysis_complete": True,
                "directory_listed": directory_listed,
                "files_read": files_read,
                "files_analyzed": files_analyzed
            }

        # Get tools and setup model
        client = await get_mcp_client()
        tools = await client.get_tools()
        model_with_tools = model.bind_tools(tools)

        # Prepare messages with enhanced context
        messages = state['messages']
        if not messages:
            messages = [HumanMessage(
                content=f"I need to analyze files to answer: '{state['question']}'. Please start by listing the directory contents."
            )]

        # Enhanced context for the prompt
        context = {
            'directory_listed': directory_listed,
            'files_read': files_read,
            'iteration': state['iteration'],
            'findings': state.get('findings', '')
        }

        research_prompt = get_research_prompt(state['question'], context)
        all_messages = [SystemMessage(content=research_prompt)] + messages

        # Call LLM with progress indicator
        with Progress(SpinnerColumn(), TextColumn("Analyzing..."), console=console, transient=True):
            response = model_with_tools.invoke(all_messages)

        # Log response preview
        preview = str(response.content)[:150]
        console.print(f"[blue]Response: {preview}...[/blue]")

        return {
            **state,
            "messages": messages + [response],
            "iteration": state['iteration'] + 1,
            "should_continue": True,
            "directory_listed": directory_listed,
            "files_read": files_read,
            "files_analyzed": files_analyzed
        }

    except Exception as e:
        console.print(f"[red]Research error: {e}[/red]")
        logger.error(f"Research step error: {e}")
        return {
            **state,
            "should_continue": False,
            "analysis_complete": True,
            "error_count": state.get('error_count', 0) + 1
        }


async def tool_execution_step(state: AgentState) -> AgentState:
    """Enhanced tool execution with better error handling and progress tracking"""
    try:
        messages = state['messages']
        if not messages:
            return {**state, "should_continue": False}

        last_message = messages[-1]
        if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
            console.print("[yellow]No tools to execute - proceeding to analysis[/yellow]")
            return {**state, "should_continue": False, "analysis_complete": True}

        console.print(f"[blue]Executing {len(last_message.tool_calls)} tool(s)...[/blue]")

        client = await get_mcp_client()
        tools = await client.get_tools()
        tools_by_name = {tool.name: tool for tool in tools}

        tool_messages = []
        files_analyzed = list(state.get('files_analyzed', []))

        # Progress tracking for tool execution
        with Progress(console=console) as progress:
            task = progress.add_task("Executing tools...", total=len(last_message.tool_calls))

            for i, tool_call in enumerate(last_message.tool_calls):
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_id = tool_call.get("id")

                progress.update(task, advance=1, description=f"Running {tool_name}...")

                if tool_name in tools_by_name:
                    try:
                        tool = tools_by_name[tool_name]
                        result = await tool.ainvoke(tool_args)
                        result_str = str(result)

                        # Track files being read
                        if tool_name in ["read_file", "read_text_file"] and "path" in tool_args:
                            filename = Path(tool_args["path"]).name
                            if filename not in files_analyzed:
                                files_analyzed.append(filename)

                        # Smart truncation of results for logging
                        if len(result_str) > 500:
                            preview = result_str[:200] + f"\n... (truncated, total: {len(result_str)} chars) ..."
                        else:
                            preview = result_str

                        console.print(f"[green]{tool_name} completed[/green]")

                        tool_messages.append(ToolMessage(
                            content=result_str,
                            name=tool_name,
                            tool_call_id=tool_id
                        ))
                    except Exception as e:
                        console.print(f"[red]Tool {tool_name} error: {e}[/red]")
                        tool_messages.append(ToolMessage(
                            content=f"Error executing {tool_name}: {e}",
                            name=tool_name,
                            tool_call_id=tool_id
                        ))

        # Update comprehensive state
        directory_listed, files_read, _ = analyze_state_from_messages(messages + tool_messages)

        return {
            **state,
            "messages": messages + tool_messages,
            "directory_listed": directory_listed,
            "files_read": files_read,
            "files_analyzed": files_analyzed,
            "should_continue": True
        }

    except Exception as e:
        console.print(f"[red]Tool execution error: {e}[/red]")
        logger.error(f"Tool execution error: {e}")
        return {
            **state,
            "should_continue": False,
            "error_count": state.get('error_count', 0) + 1
        }


async def summary_step(state: AgentState) -> AgentState:
    """Enhanced summary with comprehensive analysis"""
    try:
        messages = state['messages']
        question = state['question']
        files_analyzed = state.get('files_analyzed', [])

        # Enhanced summary prompt with file context
        summary_prompt = get_summary_prompt(question, files_analyzed)
        summary_messages = [
                               SystemMessage(content=summary_prompt)
                           ] + messages + [
                               HumanMessage(
                                   content=f"Provide a comprehensive analysis answering: '{question}'. "
                                           f"Base your response on the {len(files_analyzed)} files you analyzed: {', '.join(files_analyzed)}"
                               )
                           ]

        console.print("[blue]Generating comprehensive summary...[/blue]")

        with Progress(SpinnerColumn(), TextColumn("Creating final analysis..."), console=console, transient=True):
            response = model.invoke(summary_messages)

        console.print("[green]Analysis complete![/green]")

        return {
            **state,
            "messages": messages + [response],
            "analysis_complete": True,
            "findings": str(response.content)
        }
    except Exception as e:
        console.print(f"[red]Summary generation error: {e}[/red]")
        logger.error(f"Summary error: {e}")
        return {
            **state,
            "analysis_complete": True,
            "error_count": state.get('error_count', 0) + 1
        }


# Enhanced routing functions
def should_continue_research(state: AgentState) -> str:
    """Enhanced routing logic"""
    if not state.get('should_continue', True) or state.get('analysis_complete', False):
        return "summary"

    messages = state.get('messages', [])
    if not messages:
        return "summary"

    # Check for errors
    if state.get('error_count', 0) >= 3:
        console.print("[red]Too many errors, proceeding to summary[/red]")
        return "summary"

    last_msg = messages[-1]
    has_tool_calls = hasattr(last_msg, 'tool_calls') and last_msg.tool_calls

    if has_tool_calls:
        return "tools"
    else:
        return "summary"


def should_continue_after_tools(state: AgentState) -> str:
    """Decide whether to continue research after tool execution"""
    # Check if we have sufficient information
    files_read = state.get('files_read', 0)
    iteration = state.get('iteration', 0)

    if files_read >= 3 or iteration >= 4:
        console.print("[yellow]Sufficient information gathered, moving to summary[/yellow]")
        return "summary"

    return "research"


async def main(user_question: str = None, max_iterations: int = 5, directory: str = None):
    """Enhanced main function with more configuration options"""
    global FILES_DIRECTORY

    if directory:
        FILES_DIRECTORY = directory

    # Get user question if not provided
    if not user_question:
        console.print(Panel("[bold cyan]Enhanced Question-Driven File Research Agent[/bold cyan]"))
        user_question = input("\nWhat question would you like me to research from your files? \n> ")

    if not user_question.strip():
        console.print("[red]Please provide a valid question![/red]")
        return

    # Display configuration
    config_table = Table(title="Research Configuration")
    config_table.add_column("Parameter", style="cyan")
    config_table.add_column("Value", style="green")
    config_table.add_row("Question", user_question)
    config_table.add_row("Directory", FILES_DIRECTORY)
    config_table.add_row("Max Iterations", str(max_iterations))
    console.print(config_table)

    # Build the StateGraph
    workflow = StateGraph(AgentState)

    # Add nodes
    workflow.add_node("research", research_step)
    workflow.add_node("tools", tool_execution_step)
    workflow.add_node("summary", summary_step)

    # Add edges
    workflow.add_edge(START, "research")
    workflow.add_conditional_edges(
        "research",
        should_continue_research,
        {
            "tools": "tools",
            "summary": "summary"
        }
    )
    workflow.add_conditional_edges(
        "tools",
        should_continue_after_tools,
        {
            "research": "research",
            "summary": "summary"
        }
    )
    workflow.add_edge("summary", END)

    # Compile the graph
    app = workflow.compile()

    try:
        console.print("[green]Starting enhanced file analysis...[/green]")

        # Enhanced initial state
        initial_state: AgentState = {
            "messages": [],
            "iteration": 0,
            "directory_listed": False,
            "files_read": 0,
            "should_continue": True,
            "analysis_complete": False,
            "question": user_question,
            "files_analyzed": [],
            "findings": "",
            "error_count": 0,
            "max_iterations": max_iterations
        }

        # Run the workflow
        config = {"recursion_limit": max_iterations * 2}

        start_time = asyncio.get_event_loop().time()
        result = await app.ainvoke(initial_state, config=config)
        end_time = asyncio.get_event_loop().time()

        # Display comprehensive results
        if result.get("messages"):
            last_msg = result["messages"][-1]
            if hasattr(last_msg, 'content'):
                console.print("\n" + "=" * 80)
                console.print(Panel(
                    str(last_msg.content),
                    title=f"RESEARCH RESULTS: {user_question[:50]}{'...' if len(user_question) > 50 else ''}",
                    border_style="green",
                    padding=(1, 2)
                ))

        # Enhanced statistics
        stats_table = Table(title="Research Statistics", show_header=True)
        stats_table.add_column("Metric", style="cyan")
        stats_table.add_column("Value", style="green")

        stats_table.add_row("Total Time", f"{end_time - start_time:.2f} seconds")
        stats_table.add_row("Iterations", str(result.get('iteration', 0)))
        stats_table.add_row("Files Analyzed", str(len(result.get('files_analyzed', []))))
        stats_table.add_row("Files Names", ", ".join(result.get('files_analyzed', [])) or "None")
        stats_table.add_row("Errors", str(result.get('error_count', 0)))
        stats_table.add_row("Status", "Complete" if result.get('analysis_complete') else "Incomplete")

        console.print(stats_table)

    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        logger.error(f"Main execution error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # Enhanced example usage with more flexibility
    import sys

    # Check for command line arguments
    question = None
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])

    # Run with custom question or prompt user
    asyncio.run(main(
        user_question=question,
        max_iterations=5,
        directory=None  # Uses default FILES_DIRECTORY
    ))