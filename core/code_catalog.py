"""
Navigation catalog for the Framework Learning screen.
Defines every framework → project → files hierarchy.
"""
from pathlib import Path

CODE_PROJECTS_DIR = Path(__file__).parent.parent / "data" / "code_projects"

CODE_CATALOG = {
    "openai_sdk": {
        "label": "OpenAI Agents SDK",
        "color": "green",
        "tagline": "Week 2 — native async agents with structured outputs",
        "key_concept": "Agent + Runner.run() + Pydantic output types + handoffs",
        "why_learn": (
            "The OpenAI Agents SDK is the simplest mental model: one agent, one run. "
            "Mastering it first makes CrewAI and LangGraph easier to understand by contrast."
        ),
        "projects": [
            {
                "id": "deep_research",
                "label": "Deep Research Agent",
                "description": (
                    "Async pipeline: user query → Planner agent designs searches → "
                    "Search agents execute in parallel → Writer agent synthesises report → "
                    "Email agent delivers it."
                ),
                "flow": "deep_research.py → research_manager.py → planner_agent → search_agents → writer_agent → email_agent",
                "key_patterns": [
                    "Agent(name, instructions, model, output_type) — the atom of OpenAI SDK",
                    "Runner.run(agent, input) — synchronous execution",
                    "Pydantic BaseModel as output_type — structured, type-safe results",
                    "Parallel async fan-out with asyncio.gather()",
                    "trace() + gen_trace_id() — native OpenAI tracing dashboard",
                ],
                "files": [
                    {
                        "name": "research_manager.py",
                        "role": "Orchestrator — owns the full pipeline, calls all other agents in sequence",
                        "order": 1,
                    },
                    {
                        "name": "planner_agent.py",
                        "role": "Designs the web search plan — outputs structured WebSearchPlan Pydantic model",
                        "order": 2,
                    },
                    {
                        "name": "search_agent.py",
                        "role": "Executes a single web search — uses WebSearchTool, returns SearchResult",
                        "order": 3,
                    },
                    {
                        "name": "writer_agent.py",
                        "role": "Synthesises all search results into a final markdown report",
                        "order": 4,
                    },
                    {
                        "name": "email_agent.py",
                        "role": "Sends the final report via email — tool-using agent",
                        "order": 5,
                    },
                    {
                        "name": "deep_research.py",
                        "role": "Gradio UI entry point — launches the app and connects UI to research_manager",
                        "order": 6,
                    },
                ],
            }
        ],
    },

    "crewai": {
        "label": "CrewAI",
        "color": "orange",
        "tagline": "Week 3 — config-driven multi-agent crews with YAML",
        "key_concept": "@CrewBase + @agent + @task + @crew decorators + agents.yaml / tasks.yaml",
        "why_learn": (
            "CrewAI separates 'what agents do' (YAML) from 'how they connect' (Python). "
            "This is production-friendly: non-engineers can tweak agent behaviour without touching code."
        ),
        "projects": [
            {
                "id": "coder",
                "label": "Coder Agent",
                "description": "Single agent that writes and executes Python code safely in Docker. Shows code execution mode.",
                "flow": "main.py → Coder().crew().kickoff() → coding_task → coder agent executes code in Docker",
                "key_patterns": [
                    "allow_code_execution=True — agent can run code",
                    "code_execution_mode='safe' — Docker sandbox",
                    "YAML config drives agent role/goal/backstory",
                    "max_retry_limit — automatic retry on failure",
                ],
                "files": [
                    {"name": "crew.py",      "role": "Crew definition with @agent, @task, @crew decorators", "order": 1},
                    {"name": "agents.yaml",  "role": "Agent persona: role, goal, backstory — all text, no code", "order": 2},
                    {"name": "tasks.yaml",   "role": "Task description and expected output — wires to agent", "order": 3},
                    {"name": "main.py",      "role": "Entry point — calls Coder().crew().kickoff(inputs={})", "order": 4},
                    {"name": "custom_tool.py", "role": "Example custom tool using @tool decorator", "order": 5},
                ],
            },
            {
                "id": "debate",
                "label": "Debate Crew",
                "description": "Three agents — Proposer, Opposer, Judge — debate a topic sequentially. Classic multi-agent handoff.",
                "flow": "main.py → Debate crew → propose_task → oppose_task → decide_task",
                "key_patterns": [
                    "Process.sequential — tasks run in order, each sees previous output",
                    "context=[previous_task] — task can reference output of earlier tasks",
                    "Multiple agents collaborating on one goal",
                    "output_file — each task writes markdown to disk",
                ],
                "files": [
                    {"name": "crew.py",     "role": "Defines 3 agents (debater×2, judge) and 3 tasks in sequence", "order": 1},
                    {"name": "agents.yaml", "role": "Personas for debater and judge roles", "order": 2},
                    {"name": "tasks.yaml",  "role": "propose / oppose / decide tasks with context dependencies", "order": 3},
                    {"name": "main.py",     "role": "Entry point with topic input", "order": 4},
                ],
            },
            {
                "id": "engineering_team",
                "label": "Engineering Team",
                "description": "Software engineering crew: Architect designs, Engineer implements, QA writes tests. Produces real working code.",
                "flow": "main.py → EngineeringTeam crew → design_task → code_task → test_task",
                "key_patterns": [
                    "Multi-role specialisation — each agent has distinct expertise",
                    "Task context chaining — engineer sees architect output",
                    "output_pydantic — structured code output with validation",
                    "allow_code_execution on engineer agent",
                ],
                "files": [
                    {"name": "crew.py",       "role": "Architect + Engineer + QA agents, 3 sequential tasks", "order": 1},
                    {"name": "agents.yaml",   "role": "Specialist personas for each engineering role", "order": 2},
                    {"name": "tasks.yaml",    "role": "design/code/test tasks with context linkage", "order": 3},
                    {"name": "main.py",       "role": "Entry point — pass assignment, get working code", "order": 4},
                    {"name": "custom_tool.py","role": "File write tool used by engineer agent", "order": 5},
                ],
            },
            {
                "id": "financial_researcher",
                "label": "Financial Researcher",
                "description": "Researches a company using web search and produces a detailed investment report. Introduces external tools.",
                "flow": "main.py → FinancialResearcher crew → research_task (web search) → report_task",
                "key_patterns": [
                    "SerperDevTool — real-time web search integration",
                    "tools=[...] on specific agents — tool-aware agents",
                    "Long-form structured output via output_file",
                    "Internet-connected agents vs. knowledge-only agents",
                ],
                "files": [
                    {"name": "crew.py",     "role": "Researcher + Analyst agents; researcher gets SerperDevTool", "order": 1},
                    {"name": "agents.yaml", "role": "Researcher and analyst personas with web access", "order": 2},
                    {"name": "tasks.yaml",  "role": "Research task feeds into analysis task", "order": 3},
                    {"name": "main.py",     "role": "Entry point — pass company name, get report", "order": 4},
                ],
            },
            {
                "id": "stock_picker",
                "label": "Stock Picker",
                "description": "Most complex CrewAI project: LongTermMemory + ShortTermMemory + EntityMemory with RAG storage. Trending company finder + investment analyst.",
                "flow": "main.py → StockPicker crew (memory enabled) → trending_task → analysis_task → decision_task",
                "key_patterns": [
                    "LongTermMemory + ShortTermMemory + EntityMemory — full memory stack",
                    "RAGStorage — memory backed by vector DB",
                    "memory=True on agents — agents recall past runs",
                    "push_tool — custom tool that writes outputs",
                    "Most production-realistic pattern in the course",
                ],
                "files": [
                    {"name": "crew.py",     "role": "3 agents with full memory config — most advanced crew", "order": 1},
                    {"name": "agents.yaml", "role": "Trending finder + analyst + decision maker personas", "order": 2},
                    {"name": "tasks.yaml",  "role": "3 sequential tasks: find → analyse → decide", "order": 3},
                    {"name": "main.py",     "role": "Entry point — kicks off crew, shows memory in action", "order": 4},
                    {"name": "push_tool.py","role": "Custom tool that saves outputs — shows tool authoring pattern", "order": 5},
                ],
            },
        ],
    },

    "langgraph": {
        "label": "LangGraph",
        "color": "blue",
        "tagline": "Week 4 — explicit graph-based stateful agents with conditional routing",
        "key_concept": "StateGraph + nodes + edges + MemorySaver checkpointing",
        "why_learn": (
            "LangGraph gives you the most control: you draw the exact decision graph. "
            "It's what production systems at scale use when agent flow needs to be auditable and persistent."
        ),
        "projects": [
            {
                "id": "adriana_sidekick",
                "label": "Event Planner Sidekick",
                "description": "Conversational event planning agent with tools, memory (MemorySaver), and conditional routing. Clean complete example of the sidekick pattern.",
                "flow": "app.py → compiled_graph.ainvoke() → [tool_node | llm_node] → conditional edge → END or loop",
                "key_patterns": [
                    "StateGraph(State) — graph typed by a state class",
                    "add_messages reducer — state accumulates messages automatically",
                    "ToolNode — wraps tools, auto-called when LLM emits tool_calls",
                    "Conditional edges — route based on whether LLM wants tools or is done",
                    "MemorySaver checkpointer — persistent conversation per thread_id",
                    "compiled_graph.ainvoke() with config={'configurable': {'thread_id': ...}}",
                ],
                "files": [
                    {"name": "sidekick.py",       "role": "Core: StateGraph definition, nodes, edges, compile with MemorySaver", "order": 1},
                    {"name": "sidekick_tools.py", "role": "Tool definitions using @tool decorator — what the agent can do", "order": 2},
                    {"name": "app.py",            "role": "Gradio UI — streams graph output to user in real time", "order": 3},
                ],
            },
            {
                "id": "codekick",
                "label": "Code Assistant (Codekick)",
                "description": "Multi-node code generation graph: orchestrator routes to specialist nodes (write, read, execute). Shows complex conditional routing.",
                "flow": "app.py → graph.ainvoke() → orchestrator → conditional → [write_node | read_node | exec_node] → loop back or END",
                "key_patterns": [
                    "Multi-node graph — each node is a specialist function",
                    "Orchestrator node — decides which tool node to call next",
                    "TypedDict State with multiple fields (not just messages)",
                    "create_react_agent() prebuilt pattern vs. manual graph",
                    "File system tools (write_file, read_file) as graph nodes",
                    "Groq LLM swap — LangGraph is LLM-provider agnostic",
                ],
                "files": [
                    {"name": "states.py",       "role": "State TypedDict definition — the data flowing through the graph", "order": 1},
                    {"name": "graph.py",        "role": "Full StateGraph: all nodes, all edges, compile", "order": 2},
                    {"name": "orchestrator.py", "role": "The router node — decides what to do next", "order": 3},
                    {"name": "tools.py",        "role": "File I/O tools as LangChain @tool functions", "order": 4},
                    {"name": "prompts.py",      "role": "System prompts for each node — shows prompt engineering in graphs", "order": 5},
                ],
            },
        ],
    },
}


def get_catalog():
    return CODE_CATALOG


def get_file_path(framework: str, project: str, filename: str) -> Path | None:
    """Return absolute path to a code file, or None if not found."""
    path = CODE_PROJECTS_DIR / framework / project / filename
    return path if path.exists() else None


def get_project(framework: str, project_id: str) -> dict | None:
    fw = CODE_CATALOG.get(framework)
    if not fw:
        return None
    for p in fw["projects"]:
        if p["id"] == project_id:
            return p
    return None
