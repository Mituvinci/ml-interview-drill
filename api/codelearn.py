"""
Framework Learning endpoints — browse code, get Claude explanations.
GET  /api/codelearn/catalog        → full framework/project/file tree
GET  /api/codelearn/file           → raw code content
POST /api/codelearn/explain        → Claude walkthrough (cached)
"""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import anthropic

from core.code_catalog import get_catalog, get_file_path, get_project
from core.rag import retrieve_chunks, format_chunks_for_prompt
from core.hf_sync import push

router = APIRouter()
MODEL = "claude-sonnet-4-20250514"
CACHE_FILE = Path(__file__).parent.parent / "data" / "code_explanations.json"


# ── Cache helpers ─────────────────────────────────────────────────

def _load_cache() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}


def _save_cache(data: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, indent=2))
    push("code_explanations.json")


# ── Endpoints ─────────────────────────────────────────────────────

@router.get("/codelearn/catalog")
def get_code_catalog():
    """Return the full framework → project → file navigation tree."""
    return get_catalog()


@router.get("/codelearn/file")
def get_code_file(framework: str, project: str, file: str):
    """Return raw content of a specific code file."""
    path = get_file_path(framework, project, file)
    if not path:
        raise HTTPException(status_code=404, detail=f"File not found: {framework}/{project}/{file}")
    return {
        "framework": framework,
        "project": project,
        "file": file,
        "content": path.read_text(encoding="utf-8", errors="replace"),
        "language": "yaml" if file.endswith(".yaml") else "python",
    }


class ExplainRequest(BaseModel):
    framework: str
    project: str
    file: str
    force_refresh: bool = False


@router.post("/codelearn/explain")
def explain_code_file(req: ExplainRequest):
    """
    Claude explains a code file in depth: imports, logic flow, patterns,
    how it fits the project, and interview questions.
    Results are cached per file.
    """
    cache_key = f"{req.framework}/{req.project}/{req.file}"
    cache = _load_cache()

    if cache_key in cache and not req.force_refresh:
        return {"explanation": cache[cache_key], "from_cache": True}

    # Get file content
    path = get_file_path(req.framework, req.project, req.file)
    if not path:
        raise HTTPException(status_code=404, detail=f"File not found: {cache_key}")
    code = path.read_text(encoding="utf-8", errors="replace")

    # Get project metadata for context
    proj = get_project(req.framework, req.project)
    proj_context = ""
    if proj:
        file_meta = next((f for f in proj["files"] if f["name"] == req.file), None)
        proj_context = (
            f"Project: {proj['label']}\n"
            f"Description: {proj['description']}\n"
            f"Flow: {proj['flow']}\n"
            f"This file's role: {file_meta['role'] if file_meta else 'unknown'}\n"
        )

    # RAG: find relevant book/course passages about these patterns
    rag_query = f"{req.framework} {req.file.replace('.py','').replace('.yaml','')} agent workflow"
    chunks = retrieve_chunks(query=rag_query, n_results=2)
    book_context = format_chunks_for_prompt(chunks)

    framework_labels = {
        "openai_sdk": "OpenAI Agents SDK",
        "crewai": "CrewAI",
        "langgraph": "LangGraph",
    }
    fw_label = framework_labels.get(req.framework, req.framework)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=2000,
        temperature=0,
        system=(
            "You are an expert in agentic AI frameworks teaching a PhD student "
            "who is preparing for ML Engineer / Research Scientist interviews at Google. "
            "She has watched the course videos and run the code but wants to deeply understand "
            "the patterns, not just execute them. "
            "Use code references (function names, class names, line logic) throughout. "
            "Be specific and direct. Avoid generic descriptions."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Framework: **{fw_label}**\n"
                f"{proj_context}\n"
                f"File: `{req.file}`\n\n"
                f"```python\n{code}\n```\n\n"
                f"Relevant course/book context:\n{book_context}\n\n"
                "Explain this file thoroughly using this structure:\n\n"
                "## 1. What This File Does\n"
                "One paragraph: its single responsibility in the project.\n\n"
                "## 2. Key Imports — Why Each One Matters\n"
                "For each import: what it is, why it's needed here, what breaks without it.\n\n"
                "## 3. Core Logic Walkthrough\n"
                "Walk through the code top-to-bottom. For each function/class/block:\n"
                "- What it does\n"
                "- Any non-obvious design choices\n"
                "- What data goes in and comes out\n\n"
                "## 4. How It Fits the Project\n"
                "Where does this file sit in the execution flow? What calls it, what does it call?\n\n"
                "## 5. The Key Pattern to Remember\n"
                "What is the ONE thing from this file that you'd use in your own projects?\n\n"
                "## 6. Interview Questions\n"
                "2 interview questions this file prepares you to answer, with concise answers."
            ),
        }],
    )

    explanation = message.content[0].text.strip()
    cache[cache_key] = explanation
    _save_cache(cache)

    return {"explanation": explanation, "from_cache": False}
