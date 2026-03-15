"""
Study journal — logs every drill session by date in data/journal.json.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

JOURNAL_FILE = Path(__file__).parent.parent / "data" / "journal.json"


def _load() -> dict:
    if JOURNAL_FILE.exists():
        return json.loads(JOURNAL_FILE.read_text())
    return {"sessions": []}


def _save(data: dict):
    JOURNAL_FILE.parent.mkdir(parents=True, exist_ok=True)
    JOURNAL_FILE.write_text(json.dumps(data, indent=2))


def _today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def _now_time() -> str:
    return datetime.now(timezone.utc).strftime("%H:%M:%S")


def _session_id(date: str) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return f"sess_{ts}"


def log_entry(question_id: int, question_text: str, tag: str,
              score: int, verdict: str, cache_key: str):
    """Append an entry to today's journal session."""
    data = _load()
    today = _today()

    # Find or create today's session
    sessions = data["sessions"]
    session = next((s for s in sessions if s["date"] == today), None)
    if session is None:
        session = {
            "date": today,
            "session_id": _session_id(today),
            "entries": [],
            "summary": {"questions_attempted": 0, "avg_score": 0.0, "topics_covered": []},
        }
        sessions.append(session)

    entry = {
        "time": _now_time(),
        "question_id": question_id,
        "question_text": question_text,
        "topic_tag": tag,
        "score": score,
        "verdict": verdict,
        "cache_key": cache_key,
    }
    session["entries"].append(entry)

    # Update summary
    scores = [e["score"] for e in session["entries"]]
    topics = list({e["topic_tag"] for e in session["entries"]})
    session["summary"] = {
        "questions_attempted": len(session["entries"]),
        "avg_score": round(sum(scores) / len(scores), 1),
        "topics_covered": topics,
    }

    _save(data)


def get_all_sessions() -> list:
    data = _load()
    return sorted(data["sessions"], key=lambda s: s["date"], reverse=True)
