from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

load_dotenv()

from api.drill import router as drill_router
from api.evaluate import router as evaluate_router
from api.progress import router as progress_router
from api.journal import router as journal_router
from api.exercises import router as exercises_router
from api.cheatsheet import router as cheatsheet_router
from api.codelearn import router as codelearn_router
from api.study_guide import router as study_guide_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    from core.hf_sync import pull_all
    pull_all()
    yield


app = FastAPI(title="ML Drill", version="1.0.0", lifespan=lifespan)

app.include_router(drill_router, prefix="/api")
app.include_router(evaluate_router, prefix="/api")
app.include_router(progress_router, prefix="/api")
app.include_router(journal_router, prefix="/api")
app.include_router(exercises_router, prefix="/api")
app.include_router(cheatsheet_router, prefix="/api")
app.include_router(codelearn_router, prefix="/api")
app.include_router(study_guide_router, prefix="/api")

FRONTEND_DIR = Path(__file__).parent / "frontend"

app.mount("/frontend", StaticFiles(directory=str(FRONTEND_DIR)), name="frontend")


@app.get("/")
def serve_frontend():
    return FileResponse(str(FRONTEND_DIR / "index.html"))


NOTES_DIR = Path(__file__).parent / "notes"
ALLOWED_NOTES = {
    "iangoodfellow_chapter_2_linear_algebra_notes_1.html",
}


@app.get("/notes/{filename}")
def serve_note(filename: str):
    """Serve personal study notes HTML files. Private — not linked publicly."""
    if filename not in ALLOWED_NOTES:
        raise HTTPException(status_code=404, detail="Note not found")
    path = NOTES_DIR / filename
    if not path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(str(path), media_type="text/html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/api/sync-test")
def sync_test():
    """Diagnostic: check HF sync status and try a test push of progress.json."""
    from core.hf_sync import get_status, push
    status = get_status()
    if status["enabled"]:
        result = push("progress.json")
        status["test_push"] = result
    return status
