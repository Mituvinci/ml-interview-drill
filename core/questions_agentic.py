# Agentic AI — Weeks 1-6 course material
# Covers: LLM fundamentals, agents, tool use, memory, RAG,
# multi-agent systems (CrewAI, AutoGen, LangGraph), MCP

AGENTIC_QUESTIONS = [
    # ── LLM FUNDAMENTALS ───────────────────────────────────────────
    {
        "id": 401,
        "text": "What is the transformer architecture? Explain self-attention, multi-head attention, and positional encoding.",
        "tag": "llm_fundamentals", "difficulty": "hard", "source": "Agentic Week1",
    },
    {
        "id": 402,
        "text": "What is temperature in LLM sampling? What is top-k and top-p (nucleus) sampling? How do they affect output?",
        "tag": "llm_fundamentals", "difficulty": "medium", "source": "Agentic Week1",
    },
    {
        "id": 403,
        "text": "What is a context window? What are the implications of limited context for agentic systems?",
        "tag": "llm_fundamentals", "difficulty": "medium", "source": "Agentic Week1",
    },
    {
        "id": 404,
        "text": "What is prompt engineering? Compare zero-shot, few-shot, and chain-of-thought prompting with examples.",
        "tag": "prompt_engineering", "difficulty": "medium", "source": "Agentic Week1",
    },

    # ── AGENT ARCHITECTURE ─────────────────────────────────────────
    {
        "id": 405,
        "text": "What is an AI agent? What are the core components: perception, memory, planning, and action?",
        "tag": "agent_architecture", "difficulty": "medium", "source": "Agentic Week2",
    },
    {
        "id": 406,
        "text": "What is the ReAct pattern (Reasoning + Acting)? Write the thought-action-observation loop.",
        "tag": "agent_architecture", "difficulty": "hard", "source": "Agentic Week2",
    },
    {
        "id": 407,
        "text": "What is tool use / function calling in LLM agents? How does the model decide which tool to call?",
        "tag": "tool_use", "difficulty": "medium", "source": "Agentic Week2",
    },
    {
        "id": 408,
        "text": "What are the different types of memory in AI agents: in-context, external, episodic, semantic? Compare them.",
        "tag": "agent_memory", "difficulty": "hard", "source": "Agentic Week2",
    },

    # ── RAG ────────────────────────────────────────────────────────
    {
        "id": 409,
        "text": "What is Retrieval-Augmented Generation (RAG)? Walk through the full pipeline from document ingestion to answer generation.",
        "tag": "rag", "difficulty": "hard", "source": "Agentic Week3",
    },
    {
        "id": 410,
        "text": "What is chunking strategy in RAG? How does chunk size affect retrieval quality and LLM context usage?",
        "tag": "rag", "difficulty": "medium", "source": "Agentic Week3",
    },
    {
        "id": 411,
        "text": "What is a vector database? How does approximate nearest neighbor (ANN) search work? Compare FAISS vs ChromaDB.",
        "tag": "vector_databases", "difficulty": "medium", "source": "Agentic Week3",
    },
    {
        "id": 412,
        "text": "What is hybrid search in RAG? How do you combine dense vector search with sparse BM25 retrieval?",
        "tag": "rag", "difficulty": "hard", "source": "Agentic Week3",
    },

    # ── MULTI-AGENT SYSTEMS ────────────────────────────────────────
    {
        "id": 413,
        "text": "What are multi-agent systems? What problems do they solve that single agents cannot?",
        "tag": "multi_agent", "difficulty": "medium", "source": "Agentic Week4",
    },
    {
        "id": 414,
        "text": "What is CrewAI? What are roles, tasks, and crews? When would you use CrewAI over a single agent?",
        "tag": "multi_agent", "difficulty": "medium", "source": "Agentic Week4",
    },
    {
        "id": 415,
        "text": "What is LangGraph? How does it differ from linear agent chains? Explain nodes, edges, and state management.",
        "tag": "langgraph", "difficulty": "hard", "source": "Agentic Week4",
    },
    {
        "id": 416,
        "text": "What is AutoGen? How does conversational programming work? Compare AutoGen vs CrewAI for multi-agent tasks.",
        "tag": "multi_agent", "difficulty": "medium", "source": "Agentic Week5",
    },

    # ── MCP & INFRASTRUCTURE ───────────────────────────────────────
    {
        "id": 417,
        "text": "What is the Model Context Protocol (MCP)? What problem does it solve for tool integration in AI agents?",
        "tag": "mcp", "difficulty": "medium", "source": "Agentic Week6",
    },
    {
        "id": 418,
        "text": "How do you evaluate an agentic AI system? What metrics go beyond accuracy for agent evaluation?",
        "tag": "agent_evaluation", "difficulty": "hard", "source": "Agentic Week6",
    },
    {
        "id": 419,
        "text": "What are the main failure modes of LLM agents in production? How do you add guardrails?",
        "tag": "agent_evaluation", "difficulty": "hard", "source": "Agentic Week6",
    },
    {
        "id": 420,
        "text": "What is fine-tuning vs RAG vs prompt engineering? When do you choose each approach for a production LLM application?",
        "tag": "llm_fundamentals", "difficulty": "hard", "source": "Agentic Week1",
    },
]
