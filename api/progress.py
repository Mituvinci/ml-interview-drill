import json
from pathlib import Path
from fastapi import APIRouter

router = APIRouter()
PROGRESS_FILE = Path(__file__).parent.parent / "data" / "progress.json"


def load_progress() -> dict:
    if PROGRESS_FILE.exists():
        return json.loads(PROGRESS_FILE.read_text())
    return {"sessions": [], "weak_spots": {}}


@router.get("/progress")
def get_progress():
    progress = load_progress()
    weak_spots = progress.get("weak_spots", {})

    # Compute streak (consecutive days with at least one session)
    sessions = progress.get("sessions", [])
    streak = _compute_streak(sessions)

    weak = {
        tag: stats
        for tag, stats in weak_spots.items()
        if stats.get("score_avg", 10) < 6.0
    }

    return {
        "total_attempts": sum(s.get("attempts", 0) for s in weak_spots.values()),
        "streak_days": streak,
        "weak_spots": weak,
        "all_topics": weak_spots,
        "recent_sessions": sessions[-20:],
    }


def _compute_streak(sessions: list) -> int:
    if not sessions:
        return 0
    from datetime import datetime, timedelta, timezone

    days = set()
    for s in sessions:
        try:
            dt = datetime.fromisoformat(s["timestamp"])
            days.add(dt.date())
        except Exception:
            continue

    if not days:
        return 0

    today = datetime.now(timezone.utc).date()
    streak = 0
    current = today
    while current in days:
        streak += 1
        current -= timedelta(days=1)
    return streak
