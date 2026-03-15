"""
Answer cache — stores evaluated answers permanently in data/answer_cache.json.
Key = q{question_id}_{tag}_{hash of answer[:50].lower().strip()}
"""
import json
import hashlib
from datetime import datetime
from pathlib import Path

CACHE_FILE = Path(__file__).parent.parent / "data" / "answer_cache.json"


def _make_key(question_id: int, tag: str, answer: str) -> str:
    snippet = answer[:50].lower().strip()
    h = hashlib.md5(snippet.encode()).hexdigest()[:6]
    return f"q{question_id}_{tag}_{h}"


def _load() -> dict:
    if CACHE_FILE.exists():
        return json.loads(CACHE_FILE.read_text())
    return {}


def _save(data: dict):
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    CACHE_FILE.write_text(json.dumps(data, indent=2))


def get_cached(question_id: int, tag: str, answer: str):
    """Return (cache_key, cached_entry) if found, else (cache_key, None)."""
    key = _make_key(question_id, tag, answer)
    data = _load()
    entry = data.get(key)
    if entry:
        # bump review count
        entry["times_reviewed"] = entry.get("times_reviewed", 1) + 1
        entry["last_reviewed"] = datetime.utcnow().isoformat()
        data[key] = entry
        _save(data)
    return key, entry


def save_to_cache(cache_key: str, question_id: int, question_text: str,
                  user_answer: str, evaluation: dict) -> dict:
    """Save a new evaluation result to cache. Returns the cache entry."""
    data = _load()
    entry = {
        "question_id": question_id,
        "question_text": question_text,
        "user_answer": user_answer,
        "evaluation": evaluation,
        "cached_at": datetime.utcnow().isoformat(),
        "times_reviewed": 1,
        "last_reviewed": datetime.utcnow().isoformat(),
    }
    data[cache_key] = entry
    _save(data)
    return entry


def get_by_key(cache_key: str) -> dict | None:
    return _load().get(cache_key)


def delete_key(cache_key: str):
    """Remove a cache entry so it gets re-evaluated fresh."""
    data = _load()
    data.pop(cache_key, None)
    _save(data)


# ── Book exercise cache (same file, different key prefix) ─────────

def _make_exercise_key(exercise_id: str, answer: str) -> str:
    snippet = answer[:50].lower().strip()
    h = hashlib.md5(snippet.encode()).hexdigest()[:6]
    return f"ex_{exercise_id}_{h}"


def get_cached_exercise(exercise_id: str, answer: str):
    """Return (cache_key, cached_entry) for a book exercise answer."""
    key = _make_exercise_key(exercise_id, answer)
    data = _load()
    entry = data.get(key)
    if entry:
        entry["times_reviewed"] = entry.get("times_reviewed", 1) + 1
        entry["last_reviewed"] = datetime.utcnow().isoformat()
        data[key] = entry
        _save(data)
    return key, entry


def save_exercise_cache(cache_key: str, exercise_id: str, question_text: str,
                        user_answer: str, evaluation: dict) -> dict:
    """Save a book exercise evaluation to cache."""
    data = _load()
    entry = {
        "exercise_id": exercise_id,
        "question_text": question_text,
        "user_answer": user_answer,
        "evaluation": evaluation,
        "cached_at": datetime.utcnow().isoformat(),
        "times_reviewed": 1,
        "last_reviewed": datetime.utcnow().isoformat(),
    }
    data[cache_key] = entry
    _save(data)
    return entry
