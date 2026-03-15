import json
from datetime import datetime
from pathlib import Path
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.evaluator import evaluate_answer
from core.questions import get_question
from core.question_generator import get_generated_question, GENERATED_ID_START as HARDCODED_ID_LIMIT
from core.cache import get_cached, save_to_cache, get_by_key, delete_key
from core.journal import log_entry

router = APIRouter()
PROGRESS_FILE = Path(__file__).parent.parent / "data" / "progress.json"


class EvaluateRequest(BaseModel):
    question_id: int
    answer: str
    force_refresh: bool = False


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"sessions": [], "weak_spots": {}}


def save_progress(data: dict):
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    PROGRESS_FILE.write_text(json.dumps(data, indent=2))


def update_weak_spots(progress: dict, tag: str, score: int):
    spots = progress.setdefault("weak_spots", {})
    entry = spots.setdefault(tag, {"attempts": 0, "correct": 0, "score_avg": 0.0})
    n = entry["attempts"]
    entry["score_avg"] = (entry["score_avg"] * n + score) / (n + 1)
    entry["attempts"] += 1
    if score >= 7:
        entry["correct"] += 1


@router.post("/evaluate")
def evaluate(req: EvaluateRequest):
    if req.question_id > HARDCODED_ID_LIMIT:
        question = get_generated_question(req.question_id)
    else:
        question = get_question(req.question_id)
    if question is None:
        raise HTTPException(status_code=404, detail="Question not found")

    tag = question["tag"]
    from_cache = False
    cache_key, cached = get_cached(req.question_id, tag, req.answer)

    if cached and not req.force_refresh:
        result = cached["evaluation"]
        from_cache = True
    else:
        # Force refresh: remove old cache entry
        if req.force_refresh:
            delete_key(cache_key)

        try:
            result = evaluate_answer(
                question_text=question["text"],
                user_answer=req.answer,
                topic_tag=tag,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Evaluation failed: {str(e)}")

        save_to_cache(cache_key, req.question_id, question["text"], req.answer, result)

    # Always record in progress + journal
    score = result.get("score", 0)
    result_tag = result.get("topic_tag", tag)

    progress = load_progress()
    progress["sessions"].append({
        "timestamp": datetime.utcnow().isoformat(),
        "question_id": req.question_id,
        "tag": result_tag,
        "score": score,
        "verdict": result.get("verdict"),
        "from_cache": from_cache,
    })
    update_weak_spots(progress, result_tag, score)
    save_progress(progress)

    log_entry(req.question_id, question["text"], result_tag, score,
              result.get("verdict", ""), cache_key)

    from core.hf_sync import push
    push("progress.json")
    push("journal.json")
    push("answer_cache.json")

    return {**result, "from_cache": from_cache, "cache_key": cache_key}


@router.get("/cache/{cache_key}")
def get_cache_entry(cache_key: str):
    entry = get_by_key(cache_key)
    if entry is None:
        raise HTTPException(status_code=404, detail="Cache entry not found")
    return entry
