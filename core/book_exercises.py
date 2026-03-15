"""
Book exercise store — reads/writes data/book_exercises.json.
Provides access to extracted exercises and caches Claude-generated model answers.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

EXERCISES_FILE = Path(__file__).parent.parent / "data" / "book_exercises.json"


def _load() -> dict:
    if EXERCISES_FILE.exists():
        return json.loads(EXERCISES_FILE.read_text(encoding="utf-8"))
    return {}


def _save(data: dict):
    EXERCISES_FILE.parent.mkdir(parents=True, exist_ok=True)
    EXERCISES_FILE.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def get_books() -> list[dict]:
    data = _load()
    result = []
    for key, book in data.items():
        chapters = []
        for ch_num, ch_data in book.get("chapters", {}).items():
            chapters.append({
                "num": ch_num,
                "title": ch_data.get("title", ""),
                "count": len(ch_data.get("questions", [])),
            })
        chapters.sort(key=lambda x: [int(p) if p.isdigit() else p for p in x["num"].split(".")])
        result.append({"key": key, "label": book["label"], "chapters": chapters})
    return result


def get_chapter(book: str, chapter: str) -> dict | None:
    data = _load()
    return data.get(book, {}).get("chapters", {}).get(str(chapter))


def get_question(book: str, chapter: str, q_index: int) -> dict | None:
    ch = get_chapter(book, chapter)
    if ch is None:
        return None
    questions = ch.get("questions", [])
    if q_index < 0 or q_index >= len(questions):
        return None
    return questions[q_index]


def cache_model_answer(book: str, chapter: str, q_index: int, answer: str, passages: list[dict] = None):
    data = _load()
    q = data[book]["chapters"][str(chapter)]["questions"][q_index]
    q["model_answer"] = answer
    q["model_answer_passages"] = passages or []
    q["model_answer_cached_at"] = datetime.now(timezone.utc).isoformat()
    _save(data)
