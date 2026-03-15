"""
Sync data JSON files to/from a private HF Dataset for persistence
across HF Spaces container restarts.

Required env vars (set as HF Spaces secrets):
  HF_DATASET_REPO   e.g. "halima014/ml-drill-data"
  HF_TOKEN          your HF write token
"""
import os
import sys
import shutil
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"

SYNC_FILES = [
    "progress.json",
    "journal.json",
    "answer_cache.json",
    "generated_questions.json",
    "cheatsheet_explanations.json",
    "code_explanations.json",
]


def _repo() -> str:
    return os.environ.get("HF_DATASET_REPO", "")

def _token() -> str:
    return os.environ.get("HF_TOKEN", "")

def _enabled() -> bool:
    return bool(_repo() and _token())


def get_status() -> dict:
    """Return diagnostic info — used by /api/sync-test endpoint."""
    repo = _repo()
    token = _token()
    status = {
        "enabled": bool(repo and token),
        "HF_DATASET_REPO": repo if repo else "NOT SET",
        "HF_TOKEN": ("set (" + token[:8] + "...)") if token else "NOT SET",
    }
    try:
        import huggingface_hub
        status["huggingface_hub_version"] = huggingface_hub.__version__
    except ImportError:
        status["huggingface_hub_version"] = "NOT INSTALLED"
    return status


def pull_all():
    """Download all data files from HF Dataset to local data/. Called on startup."""
    print("HF sync: checking...", flush=True)
    if not _enabled():
        print("HF sync: DISABLED — HF_DATASET_REPO or HF_TOKEN not set.", flush=True)
        return

    try:
        from huggingface_hub import HfApi
    except ImportError:
        print("HF sync: huggingface_hub not installed.", flush=True)
        return

    print(f"HF sync: pulling from {_repo()} ...", flush=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    api = HfApi()

    for filename in SYNC_FILES:
        try:
            from huggingface_hub import hf_hub_download
            cached = hf_hub_download(
                repo_id=_repo(),
                filename=filename,
                repo_type="dataset",
                token=_token(),
                force_download=True,
            )
            shutil.copy2(cached, DATA_DIR / filename)
            print(f"  pulled {filename}", flush=True)
        except Exception as e:
            print(f"  {filename}: not in dataset yet ({type(e).__name__})", flush=True)


def push(filename: str) -> dict:
    """Upload one data file to HF Dataset. Returns result dict."""
    if not _enabled():
        return {"ok": False, "reason": "disabled"}

    try:
        from huggingface_hub import HfApi
    except ImportError:
        return {"ok": False, "reason": "huggingface_hub not installed"}

    local_path = DATA_DIR / filename
    if not local_path.exists():
        return {"ok": False, "reason": f"{filename} does not exist locally"}

    try:
        api = HfApi()
        api.upload_file(
            path_or_fileobj=str(local_path),
            path_in_repo=filename,
            repo_id=_repo(),
            repo_type="dataset",
            token=_token(),
        )
        print(f"HF sync: pushed {filename} to {_repo()}", flush=True)
        return {"ok": True, "file": filename}
    except Exception as e:
        msg = f"{type(e).__name__}: {e}"
        print(f"HF sync: PUSH FAILED for {filename}: {msg}", flush=True, file=sys.stderr)
        return {"ok": False, "reason": msg}
