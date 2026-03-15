"""Study guide endpoint — serves data/study_guide.json."""
import json
from pathlib import Path
from fastapi import APIRouter, HTTPException

router = APIRouter()
GUIDE_FILE = Path(__file__).parent.parent / "data" / "study_guide.json"


@router.get("/study-guide")
def get_study_guide():
    if not GUIDE_FILE.exists():
        raise HTTPException(status_code=404, detail="Study guide not found")
    return json.loads(GUIDE_FILE.read_text(encoding="utf-8"))
