import os
import asyncio
import json
from pathlib import Path
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.messages import SystemMessage, HumanMessage, ToolMessage
from langgraph.graph import StateGraph, START, END
from typing import TypedDict, List, Annotated, Optional, Dict, Any, Union
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
import operator
import logging
from dataclasses import dataclass, field
from datetime import datetime
import hashlib
import time

import mimetypes


# Enhanced Configuration
@dataclass
class Config:
    """Centralized configuration with validation"""
    files_directory: Path
    max_iterations: int = 5
    max_files_to_read: int = 10
    max_file_size_mb: int = 50
    max_errors: int = 3
    rate_limit_requests_per_second: float = 0.2
    temperature: float = 0.1
    supported_extensions: frozenset = field(default_factory=lambda: frozenset([
        '.txt', '.md', '.json', '.csv', '.xml', '.yml', '.yaml', '.log', '.py', '.js', '.html', '.css'
    ]))

    def __post_init__(self):
        """Validate configuration"""
        if not isinstance(self.files_directory, Path):
            self.files_directory = Path(self.files_directory)

        if not self.files_directory.exists():
            raise ValueError(f"Directory does not exist: {self.files_directory}")

        if not self.files_directory.is_dir():
            raise ValueError(f"Path is not a directory: {self.files_directory}")


# Enhanced File Information
@dataclass
class FileInfo:
    """Structured file information"""
    name: str
    path: Path
    size: int
    extension: str
    mime_type: Optional[str]
    is_readable: bool
    priority_score: float = 0.0

    @classmethod
    def from_path(cls, path: Path, config: Config) -> 'FileInfo':
        """Create FileInfo from path with validation"""
        try:
            stat = path.stat()
            size = stat.st_size
            extension = path.suffix.lower()
            mime_type, _ = mimetypes.guess_type(str(path))

            # Check if file is readable
            is_readable = (
                    extension in config.supported_extensions and
                    size <= config.max_file_size_mb * 1024 * 1024 and
                    size > 0
            )

            return cls(
                name=path.name,
                path=path,
                size=size,
                extension=extension,
                mime_type=mime_type,
                is_readable=is_readable
            )
        except Exception as e:
            logging.warning(f"Could not analyze file {path}: {e}")
            return cls(
                name=path.name,
                path=path,
                size=0,
                extension="",
                mime_type=None,
                is_readable=False
            )


# Enhanced State Schema with better typing
class AgentState(TypedDict):
    messages: Annotated[List, operator.add]
    iteration: int
    files_discovered: List[FileInfo]
    files_analyzed: Annotated[List[str], operator.add]
    question: str
    findings: str
    error_count: int
    analysis_complete: bool
    should_continue: bool
    performance_metrics: Dict[str, Any]
    config: Config


# Singleton console and logger
console = Console()
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class FileAnalysisCache:
    """Simple file analysis cache to avoid re-reading files"""

    def __init__(self):
        self._cache = {}

    def _get_file_hash(self, file_path: Path) -> str:
        """Generate hash for file based on path and modification time"""
        stat = file_path.stat()
        content = f"{file_path.absolute()}_{stat.st_mtime}_{stat.st_size}"
        return hashlib.md5(content.encode()).hexdigest()

    def get(self, file_path: Path) -> Optional[str]:
        """Get cached file content"""
        try:
            file_hash = self._get_file_hash(file_path)
            return self._cache.get(file_hash)
        except Exception:
            return None

    def set(self, file_path: Path, content: str):
        """Cache file content"""
        try:
            file_hash = self._get_file_hash(file_path)
            self._cache[file_hash] = content
        except Exception:
            pass


# Global cache instance
file_cache = FileAnalysisCache()


class EnhancedMCPClient:
    """Enhanced MCP client with connection pooling and error handling"""
    _instance = None
    _client = None
    _connection_time = None

    def __new__(cls, config: Config):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get_client(self, config: Config) -> MultiServerMCPClient:
        """Get or create MCP client with connection pooling"""
        if self._client is None or self._should_reconnect():
            await self._connect(config)
        return self._client

    def _should_reconnect(self) -> bool:
        """Check if we should reconnect (e.g., connection is old)"""
        if self._connection_time is None:
            return True
        return (time.time() - self._connection_time) > 300  # 5 minutes

    async def _connect(self, config: Config):
        """Establish connection to MCP server"""
        try:
            console.print("[yellow]Connecting to MCP server...[/yellow]")

            mcp_config = {
                "filesystem": {
                    "command": "npx",
                    "args": ["-y", "@modelcontextprotocol/server-filesystem",
                             str(config.files_directory.absolute())],
                    "transport": "stdio"
                }
            }

            self._client = MultiServerMCPClient(mcp_config)
            self._connection_time = time.time()

            # Verify connection and display tools
            tools = await self._client.get_tools()
            console.print(f"[green]Connected! {len(tools)} tools available[/green]")

            # Display available tools in a nice format
            self._display_available_tools(tools)

        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            self._client = None
            raise

    def _display_available_tools(self, tools):
        """Display available MCP tools in a nice readable format"""
        if not tools:
            console.print("[yellow]No tools available from MCP server[/yellow]")
            return

        # Create tools table
        tools_table = Table(title="Available MCP Tools", show_header=True, header_style="bold blue")
        tools_table.add_column("Tool Name", style="cyan", width=20)
        tools_table.add_column("Description", style="green", width=50)
        tools_table.add_column("Parameters", style="yellow", width=30)

        for tool in tools:
            # Get tool name
            tool_name = getattr(tool, 'name', 'Unknown')

            # Get description (try various attributes)
            description = (
                    getattr(tool, 'description', None) or
                    getattr(tool, '__doc__', None) or
                    getattr(tool, 'summary', None) or
                    "No description available"
            )
            if description:
                # Truncate long descriptions
                if len(description) > 80:
                    description = description[:77] + "..."

            # Get parameters info
            params = "N/A"
            if hasattr(tool, 'args_schema'):
                schema = tool.args_schema
                if schema and hasattr(schema, '__fields__'):
                    field_names = list(schema.__fields__.keys())
                    params = ", ".join(field_names) if field_names else "None"
                elif schema and hasattr(schema, 'schema'):
                    # Handle Pydantic v2 style
                    try:
                        schema_dict = schema.schema()
                        if 'properties' in schema_dict:
                            params = ", ".join(schema_dict['properties'].keys())
                    except:
                        params = "Schema available"
            elif hasattr(tool, 'parameters'):
                # Alternative parameter access
                try:
                    if tool.parameters:
                        params = ", ".join(tool.parameters.keys())
                except:
                    pass

            tools_table.add_row(tool_name, description, params)

        # Display in a panel
        console.print(Panel(
            tools_table,
            title="MCP Server Connection Established",
            border_style="green",
            padding=(1, 2)
        ))

        # Additional info panel
        info_text = f"""
[bold cyan]Connection Details:[/bold cyan]
• Server Type: Filesystem MCP Server
• Tools Available: {len(tools)}
• Directory: {self._get_directory_info()}
• Status: Connected and Ready

[bold yellow]Usage Tips:[/bold yellow]
• Use 'list_directory' to explore available files
• Use 'read_text_file' to read file contents
• Tools are automatically available to the research agent
        """.strip()

        console.print(Panel(
            info_text,
            title="Connection Information",
            border_style="blue",
            padding=(1, 2)
        ))

    def _get_directory_info(self) -> str:
        """Get brief directory information for display"""
        try:
            # This is a bit hacky, but we need access to the config
            # In a real implementation, you might store this in the class
            return "Configured Directory"
        except:
            return "Unknown"


async def display_mcp_tools_info(config: Config):
    """Display comprehensive MCP tools information at startup"""
    try:
        console.print("\n[blue]Initializing MCP connection...[/blue]")

        # Get MCP client and tools
        mcp_client = EnhancedMCPClient(config)
        client = await mcp_client.get_client(config)
        tools = await client.get_tools()

        if not tools:
            console.print("[yellow]  No tools available from MCP server[/yellow]")
            return tools

        # Create detailed tools information
        tools_info = []
        for tool in tools:
            tool_info = {
                'name': getattr(tool, 'name', 'Unknown'),
                'description': getattr(tool, 'description', 'No description available'),
                'parameters': []
            }

            # Extract parameter information
            if hasattr(tool, 'args_schema') and tool.args_schema:
                schema = tool.args_schema
                try:
                    if hasattr(schema, '__fields__'):
                        # Pydantic v1 style
                        for field_name, field in schema.__fields__.items():
                            param_info = {
                                'name': field_name,
                                'type': str(field.type_),
                                'required': field.required,
                                'description': field.field_info.description if hasattr(field,
                                                                                       'field_info') else 'No description'
                            }
                            tool_info['parameters'].append(param_info)
                    elif hasattr(schema, 'model_fields'):
                        # Pydantic v2 style
                        for field_name, field in schema.model_fields.items():
                            param_info = {
                                'name': field_name,
                                'type': str(field.annotation) if hasattr(field, 'annotation') else 'Unknown',
                                'required': field.is_required() if hasattr(field, 'is_required') else True,
                                'description': field.description if hasattr(field, 'description') else 'No description'
                            }
                            tool_info['parameters'].append(param_info)
                except Exception as e:
                    logger.debug(f"Could not extract parameters for {tool_info['name']}: {e}")

            tools_info.append(tool_info)

        # Create comprehensive display
        main_table = Table(title="Available MCP Tools", show_header=True, header_style="bold cyan")
        main_table.add_column("Tool", style="cyan", width=18)
        main_table.add_column("Description", style="green", width=40)
        main_table.add_column("Parameters", style="yellow", width=25)
        main_table.add_column("Usage", style="magenta", width=15)

        for tool_info in tools_info:
            # Format parameters
            if tool_info['parameters']:
                params_text = "\n".join([
                    f"• {p['name']} ({p['type']}){'*' if p['required'] else ''}"
                    for p in tool_info['parameters'][:3]  # Show max 3 params
                ])
                if len(tool_info['parameters']) > 3:
                    params_text += f"\n... +{len(tool_info['parameters']) - 3} more"
            else:
                params_text = "None"

            # Truncate description
            desc = tool_info['description']
            if len(desc) > 60:
                desc = desc[:57] + "..."

            # Usage hint
            usage_hint = "Available" if tool_info['parameters'] else "Ready"

            main_table.add_row(
                tool_info['name'],
                desc,
                params_text,
                usage_hint
            )

        # Display main table
        console.print(Panel(
            main_table,
            title="MCP Filesystem Server - Connected",
            subtitle=f"Directory: {config.files_directory}",
            border_style="green",
            padding=(1, 1)
        ))

        # Create usage guide
        usage_guide = Table(title="Common Tool Usage Patterns", show_header=True)
        usage_guide.add_column("Action", style="cyan", width=25)
        usage_guide.add_column("Tool", style="yellow", width=20)
        usage_guide.add_column("Example", style="green", width=35)

        usage_guide.add_row(
            "List files in directory",
            "list_directory",
            "Shows all available files"
        )
        usage_guide.add_row(
            "Read a text file",
            "read_text_file",
            "path: '/path/to/file.txt'"
        )
        usage_guide.add_row(
            "Search within files",
            "search_files",
            "query: 'search terms'"
        )

        console.print(Panel(
            usage_guide,
            title="Usage Guide",
            border_style="blue",
            padding=(1, 1)
        ))

        return tools

    except Exception as e:
        console.print(f"[red] Failed to connect to MCP server: {e}[/red]")
        logger.error(f"MCP connection error: {e}")
        return []


class SmartFileSelector:
    """Intelligent file selection based on question relevance"""

    @staticmethod
    def calculate_relevance_score(file_info: FileInfo, question: str) -> float:
        """Calculate relevance score for a file given the question"""
        score = 0.0
        filename_lower = file_info.name.lower()
        question_lower = question.lower()

        # Keyword matching in filename
        question_words = set(question_lower.split())
        filename_words = set(filename_lower.replace('.', ' ').replace('_', ' ').replace('-', ' ').split())

        keyword_match = len(question_words.intersection(filename_words))
        score += keyword_match * 2.0

        # File type relevance
        if file_info.extension in ['.txt', '.md']:
            score += 1.0
        elif file_info.extension in ['.json', '.csv']:
            score += 0.8
        elif file_info.extension in ['.log']:
            score += 0.6

        # Size preference (medium-sized files often more informative)
        if 1000 < file_info.size < 100000:  # 1KB to 100KB
            score += 0.5
        elif file_info.size > 1000000:  # Penalize very large files
            score -= 0.5

        return score

    @classmethod
    def select_files_to_read(cls, files: List[FileInfo], question: str,
                             max_files: int = 5) -> List[FileInfo]:
        """Select most relevant files to read"""
        # Calculate scores
        for file_info in files:
            if file_info.is_readable:
                file_info.priority_score = cls.calculate_relevance_score(file_info, question)

        # Sort by score and readability
        readable_files = [f for f in files if f.is_readable]
        readable_files.sort(key=lambda x: x.priority_score, reverse=True)

        return readable_files[:max_files]


# Global LLM instance for reuse
_llm_instance = None
_llm_config_hash = None


def setup_llm(config: Config):
    """Setup LLM with caching and better configuration"""
    global _llm_instance, _llm_config_hash

    # Create a simple hash of relevant config parameters
    config_hash = hash((
        config.rate_limit_requests_per_second,
        config.temperature
    ))

    # Return cached instance if configuration hasn't changed
    if _llm_instance is not None and _llm_config_hash == config_hash:
        return _llm_instance

    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        console.print("[red]Warning: GOOGLE_API_KEY not found in environment variables[/red]")
        # You should handle this more securely in production
        api_key = "Your api key"

    rate_limiter = InMemoryRateLimiter(
        requests_per_second=config.rate_limit_requests_per_second,
        check_every_n_seconds=1,
        max_bucket_size=3
    )

    _llm_instance = init_chat_model(
        "gemini-2.0-flash",
        model_provider="google_genai",
        api_key=api_key,
        temperature=config.temperature,
        rate_limiter=rate_limiter
    )
    _llm_config_hash = config_hash

    return _llm_instance


def discover_files(config: Config) -> List[FileInfo]:
    """Enhanced file discovery with detailed analysis"""
    files = []
    try:
        for file_path in config.files_directory.rglob('*'):
            if file_path.is_file():
                file_info = FileInfo.from_path(file_path, config)
                files.append(file_info)

        # Log discovery results
        readable_count = sum(1 for f in files if f.is_readable)
        console.print(f"[blue]Discovered {len(files)} files, {readable_count} readable[/blue]")

        return files
    except Exception as e:
        logger.error(f"Error discovering files: {e}")
        return []


def create_file_summary_table(files: List[FileInfo]) -> Table:
    """Create a rich table summarizing files"""
    table = Table(title="File Analysis Summary")
    table.add_column("Filename", style="cyan", width=30)
    table.add_column("Size", style="magenta", width=10)
    table.add_column("Type", style="green", width=10)
    table.add_column("Readable", style="yellow", width=10)
    table.add_column("Priority", style="red", width=10)

    for file_info in sorted(files, key=lambda x: x.priority_score, reverse=True)[:10]:
        size_str = (f"{file_info.size} B" if file_info.size < 1024
                    else f"{file_info.size // 1024} KB")
        readable = "✓" if file_info.is_readable else "✗"
        priority = f"{file_info.priority_score:.1f}" if file_info.priority_score > 0 else "-"

        table.add_row(
            file_info.name,
            size_str,
            file_info.extension or "none",
            readable,
            priority
        )

    return table


def get_enhanced_research_prompt(state: AgentState) -> str:
    """Generate enhanced research prompt with better context"""
    question = state['question']
    iteration = state['iteration']
    files_analyzed = len(state['files_analyzed'])
    config = state['config']

    prompt = f"""You are conducting focused research to answer: "{question}"

CURRENT STATUS:
- Iteration: {iteration}/{config.max_iterations}
- Files analyzed: {files_analyzed}/{config.max_files_to_read}
- Files available: {len(state['files_discovered'])}

STRATEGY:
1. If no files listed yet: Use list_directory to see available files
2. Select files most likely to contain relevant information based on:
   - Filename relevance to the question
   - File type (prefer .txt, .md, .json, .csv)
   - Reasonable file size
3. Read 2-3 most promising files per iteration
4. Focus on extracting specific information related to: "{question}"

EFFICIENCY GUIDELINES:
- Stop after finding sufficient information (don't over-analyze)
- Prioritize quality over quantity of files read
- If you have a good answer after 2-3 files, proceed to summary

Available tools: list_directory, read_text_file, search_files"""

    return prompt


# Enhanced workflow functions
async def enhanced_research_step(state: AgentState) -> AgentState:
    """Enhanced research step with better file selection"""
    try:
        config = state['config']
        console.print(f"[blue]Research Step {state['iteration'] + 1}/{config.max_iterations}[/blue]")

        # Check termination conditions
        if (state['iteration'] >= config.max_iterations or
                len(state['files_analyzed']) >= config.max_files_to_read or
                state['error_count'] >= config.max_errors):
            return {**state, "should_continue": False, "analysis_complete": True}

        # Setup model and client
        model = setup_llm(config)
        mcp_client = EnhancedMCPClient(config)
        client = await mcp_client.get_client(config)
        tools = await client.get_tools()
        model_with_tools = model.bind_tools(tools)

        # Prepare messages
        messages = state['messages']
        if not messages:
            # Smart initial message based on file discovery
            if state['files_discovered']:
                top_files = SmartFileSelector.select_files_to_read(
                    state['files_discovered'],
                    state['question'],
                    max_files=3
                )
                file_suggestions = ", ".join([f.name for f in top_files[:3]])
                initial_msg = (f"I need to research: '{state['question']}'. "
                               f"Consider prioritizing these relevant files: {file_suggestions}")
            else:
                initial_msg = f"I need to research: '{state['question']}'. Please start by exploring available files."

            messages = [HumanMessage(content=initial_msg)]

        # Enhanced system prompt
        system_prompt = get_enhanced_research_prompt(state)
        all_messages = [SystemMessage(content=system_prompt)] + messages

        # Call LLM with timing
        start_time = time.time()
        response = model_with_tools.invoke(all_messages)
        response_time = time.time() - start_time

        # Update performance metrics
        metrics = state.get('performance_metrics', {})
        metrics['llm_call_times'] = metrics.get('llm_call_times', [])
        metrics['llm_call_times'].append(response_time)

        return {
            **state,
            "messages": messages + [response],
            "iteration": state['iteration'] + 1,
            "should_continue": True,
            "performance_metrics": metrics
        }

    except Exception as e:
        console.print(f"[red]Research error: {e}[/red]")
        logger.error(f"Research step error: {e}", exc_info=True)
        return {
            **state,
            "should_continue": False,
            "analysis_complete": True,
            "error_count": state['error_count'] + 1
        }


async def enhanced_tool_execution_step(state: AgentState) -> AgentState:
    """Enhanced tool execution with caching and better error handling"""
    try:
        messages = state['messages']
        if not messages or not hasattr(messages[-1], 'tool_calls'):
            return {**state, "should_continue": False}

        last_message = messages[-1]
        if not last_message.tool_calls:
            return {**state, "should_continue": False, "analysis_complete": True}

        config = state['config']
        mcp_client = EnhancedMCPClient(config)
        client = await mcp_client.get_client(config)
        tools = await client.get_tools()
        tools_by_name = {tool.name: tool for tool in tools}

        tool_messages = []
        files_analyzed = list(state.get('files_analyzed', []))

        with Progress(console=console) as progress:
            task = progress.add_task("Processing tools...", total=len(last_message.tool_calls))

            for tool_call in last_message.tool_calls:
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_id = tool_call.get("id")

                progress.update(task, advance=1, description=f"Running {tool_name}...")

                if tool_name not in tools_by_name:
                    continue

                try:
                    # Check cache for file reads
                    if tool_name in ["read_file", "read_text_file"] and "path" in tool_args:
                        file_path = Path(tool_args["path"])

                        # Check file size and cache
                        if file_path.exists():
                            file_size = file_path.stat().st_size
                            if file_size > config.max_file_size_mb * 1024 * 1024:
                                result = f"File too large ({file_size / 1024 / 1024:.1f}MB). Skipping."
                            else:
                                # Try cache first
                                cached_content = file_cache.get(file_path)
                                if cached_content:
                                    result = cached_content
                                    console.print(f"[green]Using cached content for {file_path.name}[/green]")
                                else:
                                    # Read file and cache
                                    tool = tools_by_name[tool_name]
                                    result = await tool.ainvoke(tool_args)
                                    file_cache.set(file_path, str(result))

                                # Track analyzed files
                                if file_path.name not in files_analyzed:
                                    files_analyzed.append(file_path.name)
                        else:
                            result = f"File not found: {file_path}"
                    else:
                        # Execute other tools normally
                        tool = tools_by_name[tool_name]
                        result = await tool.ainvoke(tool_args)

                    # Smart content truncation for very long results
                    result_str = str(result)
                    if len(result_str) > 5000:
                        truncated = result_str[
                                        :2000] + f"\n\n[TRUNCATED - Original length: {len(result_str)} chars]\n\n" + result_str[
                                        -1000:]
                        result_str = truncated

                    tool_messages.append(ToolMessage(
                        content=result_str,
                        name=tool_name,
                        tool_call_id=tool_id
                    ))

                except Exception as e:
                    error_msg = f"Error executing {tool_name}: {str(e)[:200]}"
                    console.print(f"[red]{error_msg}[/red]")
                    tool_messages.append(ToolMessage(
                        content=error_msg,
                        name=tool_name,
                        tool_call_id=tool_id
                    ))

        return {
            **state,
            "messages": messages + tool_messages,
            "files_analyzed": files_analyzed,
            "should_continue": True
        }

    except Exception as e:
        console.print(f"[red]Tool execution error: {e}[/red]")
        logger.error(f"Tool execution error: {e}", exc_info=True)
        return {
            **state,
            "should_continue": False,
            "error_count": state['error_count'] + 1
        }


def create_enhanced_summary_prompt(state: AgentState) -> str:
    """Create comprehensive summary prompt"""
    question = state['question']
    files_analyzed = state['files_analyzed']
    total_files = len(state['files_discovered'])

    return f"""Provide a comprehensive analysis for: "{question}"

ANALYSIS CONTEXT:
- Files analyzed: {len(files_analyzed)} of {total_files} available
- Analyzed files: {', '.join(files_analyzed)}

REQUIRED RESPONSE STRUCTURE:
1. **Executive Summary**: One-paragraph direct answer to the question
2. **Key Findings**: Bullet points of main discoveries from the files
3. **Evidence Sources**: Which files provided which information
4. **Confidence Assessment**: 
   - High: Strong evidence from multiple sources
   - Medium: Good evidence but limited sources  
   - Low: Insufficient or conflicting evidence
5. **Gaps & Limitations**: What information is missing or uncertain
6. **Recommendations**: If applicable, suggested next steps

GUIDELINES:
- Be specific and cite file sources
- Distinguish between facts and interpretations
- Acknowledge limitations honestly
- Focus on answering the original question directly"""


async def enhanced_summary_step(state: AgentState) -> AgentState:
    """Enhanced summary generation with comprehensive analysis"""
    try:
        model = setup_llm(state['config'])

        summary_prompt = create_enhanced_summary_prompt(state)
        messages = state['messages'] + [
            SystemMessage(content=summary_prompt),
            HumanMessage(content=f"Generate final comprehensive analysis for: '{state['question']}'")
        ]

        console.print("[blue]Generating comprehensive analysis...[/blue]")

        start_time = time.time()
        response = model.invoke(messages)
        summary_time = time.time() - start_time

        # Update performance metrics
        metrics = state.get('performance_metrics', {})
        metrics['summary_generation_time'] = summary_time
        metrics['total_files_analyzed'] = len(state['files_analyzed'])

        return {
            **state,
            "messages": state['messages'] + [response],
            "analysis_complete": True,
            "findings": str(response.content),
            "performance_metrics": metrics
        }

    except Exception as e:
        console.print(f"[red]Summary generation error: {e}[/red]")
        logger.error(f"Summary error: {e}", exc_info=True)
        return {
            **state,
            "analysis_complete": True,
            "error_count": state['error_count'] + 1
        }


# Enhanced routing functions
def should_continue_research(state: AgentState) -> str:
    """Smart routing based on state analysis"""
    if state.get('analysis_complete', False) or not state.get('should_continue', True):
        return "summary"

    if state['error_count'] >= state['config'].max_errors:
        console.print("[red]Too many errors, proceeding to summary[/red]")
        return "summary"

    messages = state.get('messages', [])
    if messages and hasattr(messages[-1], 'tool_calls') and messages[-1].tool_calls:
        return "tools"

    # Check if we have enough information
    if (len(state['files_analyzed']) >= 3 and
            state['iteration'] >= 2 and
            len(state.get('findings', '')) > 100):
        return "summary"

    return "research" if state['iteration'] < state['config'].max_iterations else "summary"


def should_continue_after_tools(state: AgentState) -> str:
    """Decide continuation after tool execution"""
    config = state['config']

    # Check limits
    if (len(state['files_analyzed']) >= config.max_files_to_read or
            state['iteration'] >= config.max_iterations):
        return "summary"

    # Check if we have sufficient information (heuristic)
    recent_messages = state['messages'][-3:] if len(state['messages']) >= 3 else state['messages']
    total_content_length = sum(len(str(msg.content)) for msg in recent_messages if hasattr(msg, 'content'))

    if total_content_length > 2000 and len(state['files_analyzed']) >= 2:
        console.print("[yellow]Sufficient information gathered[/yellow]")
        return "summary"

    return "research"


async def main(user_question: str = None, directory: str = None, max_iterations: int = 5):
    """Enhanced main function with better configuration and error handling"""
    try:
        # Setup configuration
        files_directory = Path(directory) if directory else Path(r"C:\Users\swaroopa\OneDrive\Desktop\Information")
        config = Config(
            files_directory=files_directory,
            max_iterations=max_iterations,
            max_files_to_read=10,
            max_file_size_mb=50
        )

        # Get user question
        if not user_question:
            console.print(Panel("[bold cyan]Enhanced File Research Agent v2.0[/bold cyan]"))
            user_question = input("\nWhat would you like to research from your files?\n> ").strip()

        if not user_question:
            console.print("[red]Please provide a valid question![/red]")
            return

        # File discovery and analysis
        console.print("[blue]Discovering and analyzing files...[/blue]")
        files_discovered = discover_files(config)

        if not files_discovered:
            console.print("[red]No files found in directory![/red]")
            return

        # Display MCP tools information
        await display_mcp_tools_info(config)

        # Smart file selection and prioritization
        selected_files = SmartFileSelector.select_files_to_read(files_discovered, user_question)
        for file_info in selected_files:
            file_info.priority_score = SmartFileSelector.calculate_relevance_score(file_info, user_question)

        # Display file analysis
        console.print(create_file_summary_table(files_discovered))

        # Build workflow
        workflow = StateGraph(AgentState)
        workflow.add_node("research", enhanced_research_step)
        workflow.add_node("tools", enhanced_tool_execution_step)
        workflow.add_node("summary", enhanced_summary_step)

        workflow.add_edge(START, "research")
        workflow.add_conditional_edges("research", should_continue_research, {
            "tools": "tools", "summary": "summary"
        })
        workflow.add_conditional_edges("tools", should_continue_after_tools, {
            "research": "research", "summary": "summary"
        })
        workflow.add_edge("summary", END)

        app = workflow.compile()

        # Initialize state
        initial_state: AgentState = {
            "messages": [],
            "iteration": 0,
            "files_discovered": files_discovered,
            "files_analyzed": [],
            "question": user_question,
            "findings": "",
            "error_count": 0,
            "analysis_complete": False,
            "should_continue": True,
            "performance_metrics": {"start_time": time.time()},
            "config": config
        }

        # Execute workflow
        console.print("[green]Starting enhanced file research...[/green]")
        result = await app.ainvoke(initial_state, config={"recursion_limit": max_iterations * 3})

        # Display results
        if result.get("messages") and result["messages"]:
            final_response = result["messages"][-1]
            if hasattr(final_response, 'content'):
                console.print("\n" + "=" * 100)
                console.print(Panel(
                    str(final_response.content),
                    title=f"ANALYSIS RESULTS",
                    subtitle=f"Question: {user_question[:60]}{'...' if len(user_question) > 60 else ''}",
                    border_style="green",
                    padding=(1, 2)
                ))

        # Performance metrics
        metrics = result.get('performance_metrics', {})
        total_time = time.time() - metrics.get('start_time', time.time())

        performance_table = Table(title="Performance Summary")
        performance_table.add_column("Metric", style="cyan")
        performance_table.add_column("Value", style="green")

        performance_table.add_row("Total Runtime", f"{total_time:.2f}s")
        performance_table.add_row("Iterations", str(result.get('iteration', 0)))
        performance_table.add_row("Files Discovered", str(len(files_discovered)))
        performance_table.add_row("Files Analyzed", str(len(result.get('files_analyzed', []))))
        performance_table.add_row("Error Count", str(result.get('error_count', 0)))
        performance_table.add_row("Cache Hits", str(len(file_cache._cache)))

        if 'llm_call_times' in metrics:
            avg_llm_time = sum(metrics['llm_call_times']) / len(metrics['llm_call_times'])
            performance_table.add_row("Avg LLM Response Time", f"{avg_llm_time:.2f}s")

        console.print(performance_table)

        return result

    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")
        logger.error(f"Main execution error: {e}", exc_info=True)
        return None


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else None

    asyncio.run(main(
        user_question=question,
        directory=None,  # Use default
        max_iterations=5
    ))