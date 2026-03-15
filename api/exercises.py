"""Book exercises: serve extracted exercises, generate model answers, evaluate."""
import anthropic
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.book_exercises import get_books, get_chapter, get_question, cache_model_answer
from core.cache import get_cached_exercise, save_exercise_cache, delete_key
from core.evaluator import evaluate_answer
from core.journal import log_entry
from core.rag import retrieve_chunks, format_chunks_for_prompt

router = APIRouter()
MODEL = "claude-sonnet-4-20250514"


@router.get("/exercises/books")
def list_books():
    books = get_books()
    if not books:
        raise HTTPException(
            status_code=404,
            detail="No exercises found. Run: uv run python extract_exercises.py",
        )
    return books


@router.get("/exercises/{book}/{chapter}")
def list_chapter(book: str, chapter: str):
    ch = get_chapter(book, chapter)
    if ch is None:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return {
        "title": ch.get("title", ""),
        "count": len(ch.get("questions", [])),
        "questions": [
            {
                "index": i,
                "id": q["id"],
                "text": q["text"],
                "has_model_answer": q.get("model_answer") is not None,
            }
            for i, q in enumerate(ch.get("questions", []))
        ],
    }


class ModelAnswerRequest(BaseModel):
    book: str
    chapter: str
    q_index: int
    force_refresh: bool = False


# Map exercise book keys → ChromaDB source labels (set in ingest.py BOOK_FILES)
BOOK_SOURCE_LABELS = {
    "geron":      "Geron Hands-On ML",
    "goodfellow": "Goodfellow Deep Learning",
    "chip":       "Chip Huyen Designing ML Systems",
}

MODEL_ANSWER_SYSTEM = """You are a senior ML engineer coaching a PhD candidate for top-tier MLE and Research Scientist interviews.

Write a model answer to the exercise below. Requirements:
1. INTERVIEW-READY — write the answer you'd give out loud in a technical interview: structured, confident, and clear. Not a textbook essay.
2. GROUNDED — base the answer on the provided book passages. Reference them explicitly.
3. EXAMPLES — include 1–2 concrete examples (numerical where helpful).
4. EQUATIONS — include key equations in LaTeX ($...$ inline, $$...$$ block) when they clarify the concept.
5. STRUCTURE — use ## section headers if the answer has multiple parts.
6. LENGTH — comprehensive but tight. An interviewer has 3–5 minutes.

After your answer, add a section:

## Book Evidence
For each passage you used, write one line in this exact format:
> "[short direct quote from the passage]" — {source}

Only quote passages actually provided. Do not fabricate quotes."""


@router.post("/exercises/model-answer")
def generate_model_answer(req: ModelAnswerRequest):
    q = get_question(req.book, req.chapter, req.q_index)
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found")

    if q.get("model_answer") and not req.force_refresh:
        return {
            "model_answer": q["model_answer"],
            "book_passages": q.get("model_answer_passages", []),
            "from_cache": True,
        }

    # Filter RAG to the relevant book only
    source_label = BOOK_SOURCE_LABELS.get(req.book)
    chunks = retrieve_chunks(query=q["text"], n_results=4, source_filter=source_label)
    if not chunks:
        # Fallback: search all books if this one has no indexed content
        chunks = retrieve_chunks(query=q["text"], n_results=4)
    book_context = format_chunks_for_prompt(chunks)

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        temperature=0,
        system=MODEL_ANSWER_SYSTEM,
        messages=[{
            "role": "user",
            "content": (
                f"Book: {source_label or req.book}\n"
                f"Exercise: {q['text']}\n\n"
                f"Relevant passages from the book:\n{book_context}\n\n"
                "Write the model answer:"
            ),
        }],
    )
    answer = message.content[0].text.strip()

    # Store the actual retrieved passages as evidence
    passages = [{"text": c["text"][:400], "source": c["source"]} for c in chunks]
    cache_model_answer(req.book, req.chapter, req.q_index, answer, passages)
    return {"model_answer": answer, "book_passages": passages, "from_cache": False}


class ExerciseEvaluateRequest(BaseModel):
    book: str
    chapter: str
    q_index: int
    answer: str
    force_refresh: bool = False


@router.post("/exercises/evaluate")
def evaluate_exercise(req: ExerciseEvaluateRequest):
    q = get_question(req.book, req.chapter, req.q_index)
    if q is None:
        raise HTTPException(status_code=404, detail="Question not found")

    exercise_id = q["id"]
    cache_key, cached = get_cached_exercise(exercise_id, req.answer)

    if cached and not req.force_refresh:
        return {**cached["evaluation"], "from_cache": True, "cache_key": cache_key}

    if req.force_refresh:
        delete_key(cache_key)

    try:
        result = evaluate_answer(
            question_text=q["text"],
            user_answer=req.answer,
            topic_tag="book_exercise",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

    save_exercise_cache(cache_key, exercise_id, q["text"], req.answer, result)
    log_entry(
        question_id=0,
        question_text=q["text"],
        tag=result.get("topic_tag", "book_exercise"),
        score=result.get("score", 0),
        verdict=result.get("verdict", ""),
        cache_key=cache_key,
    )

    from core.hf_sync import push
    push("answer_cache.json")
    push("journal.json")

    return {**result, "from_cache": False, "cache_key": cache_key}
