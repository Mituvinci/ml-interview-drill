from fastapi import APIRouter, HTTPException
from core.journal import get_all_sessions
from core.cache import get_by_key

router = APIRouter()


@router.get("/journal")
def get_journal():
    return get_all_sessions()


@router.get("/journal/{cache_key}")
def get_journal_entry(cache_key: str):
    entry = get_by_key(cache_key)
    if entry is None:
        raise HTTPException(status_code=404, detail="Entry not found")
    return entry
