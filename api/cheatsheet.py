"""Cheat sheet explain endpoint: Claude + RAG detailed explanation per equation."""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import anthropic
from core.rag import retrieve_chunks, format_chunks_for_prompt
from core.hf_sync import push

router = APIRouter()
MODEL = "claude-sonnet-4-20250514"
EXPLANATIONS_FILE = Path(__file__).parent.parent / "data" / "cheatsheet_explanations.json"


@router.get("/cheatsheet/data")
def get_cheatsheet_data():
    """Serve the equation cheat sheet data to the frontend."""
    from core.cheatsheet_data import CHEAT_DATA
    return CHEAT_DATA


def load_explanations() -> dict:
    if EXPLANATIONS_FILE.exists():
        return json.loads(EXPLANATIONS_FILE.read_text())
    return {}


def save_explanations(data: dict):
    EXPLANATIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    EXPLANATIONS_FILE.write_text(json.dumps(data, indent=2))
    push("cheatsheet_explanations.json")


class ExplainRequest(BaseModel):
    name: str
    tag: str
    equation: str
    symbols: str
    used: str
    force_refresh: bool = False


@router.get("/cheatsheet/explanations")
def get_all_explanations():
    return load_explanations()


@router.post("/cheatsheet/explain")
def explain_equation(req: ExplainRequest):
    explanations = load_explanations()

    if req.name in explanations and not req.force_refresh:
        return {"explanation": explanations[req.name], "from_cache": True}

    chunks = retrieve_chunks(query=f"{req.name} {req.tag} {req.used}", n_results=3)
    book_context = format_chunks_for_prompt(chunks)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=1200,
        temperature=0,
        system=(
            "You are an expert ML educator explaining equations to a PhD student "
            "preparing for ML Engineer / Research Scientist interviews. "
            "Use LaTeX for all math: $...$ for inline, $$...$$ for display equations. "
            "Always cite which book or source supports your explanation. "
            "Be precise and direct — no fluff."
        ),
        messages=[{
            "role": "user",
            "content": (
                f"Explain this equation in detail:\n\n"
                f"**{req.name}**\n"
                f"Equation: ${req.equation}$\n"
                f"Symbols: {req.symbols}\n"
                f"Used when: {req.used}\n\n"
                f"Relevant book passages:\n{book_context}\n\n"
                "Structure your answer as:\n"
                "1. **Intuition** — why does this equation make sense?\n"
                "2. **Mathematical breakdown** — what each term contributes\n"
                "3. **Worked example** — concrete numbers (small, clear)\n"
                "4. **Interview gotcha** — common mistake or trick question\n"
                "5. **Book reference** — cite the source from the passages above"
            ),
        }],
    )

    explanation = message.content[0].text.strip()
    explanations[req.name] = explanation
    save_explanations(explanations)

    return {"explanation": explanation, "from_cache": False}
