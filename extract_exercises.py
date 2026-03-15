"""
Exercise extractor: finds end-of-chapter exercises in ML book PDFs.
Run once (after ingest.py):  uv run python extract_exercises.py
Output: data/book_exercises.json

Preserves cached model_answers if you re-run.
"""
import re
import json
import fitz  # PyMuPDF
from pathlib import Path

BOOKS_DIR = Path(__file__).parent / "data" / "books"
OUTPUT = Path(__file__).parent / "data" / "book_exercises.json"

BOOKS_CONFIG = {
    "geron":      ("geron.pdf",      "Géron Hands-On ML"),
    "goodfellow": ("goodfellow.pdf", "Goodfellow Deep Learning"),
    "chip":       ("chip_huyen.pdf", "Chip Huyen Designing ML Systems"),
}


def extract_exercises(pdf_path: Path, book_key: str) -> dict[str, dict]:
    """
    Extract numbered end-of-chapter exercises from a PDF.
    Returns {chapter_str: {"title": str, "questions": list[dict]}}
    """
    doc = fitz.open(str(pdf_path))
    pages_text = [(i, page.get_text("text")) for i, page in enumerate(doc)]
    doc.close()
    total_pages = len(pages_text)

    # Regex to detect "Exercises" section heading on a page
    exercises_heading_re = re.compile(r'(?:^|\n)\s*Exercises\s*\n', re.IGNORECASE)

    # Regex to detect chapter header (various O'Reilly / Springer formats)
    chapter_header_re = re.compile(
        r'(?:^|\n)\s*(?:CHAPTER|Chapter)\s+(\d+)\s*\n\s*(.+?)(?=\n)',
        re.IGNORECASE,
    )

    # Regex to parse numbered questions: "1. text..." up to "2. text..."
    question_re = re.compile(
        r'(?m)^\s*(\d{1,2})\.\s+(.+?)(?=^\s*\d{1,2}\.\s+|\Z)',
        re.DOTALL,
    )

    chapters: dict[str, dict] = {}

    for page_idx, text in pages_text:
        if not exercises_heading_re.search(text):
            continue  # not an exercises page

        # Search backward (up to 80 pages) for the chapter this belongs to
        chapter_num = None
        chapter_title = ""
        for back_idx in range(page_idx, max(-1, page_idx - 80), -1):
            m = chapter_header_re.search(pages_text[back_idx][1])
            if m:
                chapter_num = int(m.group(1))
                chapter_title = m.group(2).strip()
                break

        if chapter_num is None:
            # Fallback: look for bare "Chapter N" anywhere in text
            for back_idx in range(page_idx, max(-1, page_idx - 80), -1):
                m = re.search(r'\bChapter\s+(\d+)\b', pages_text[back_idx][1])
                if m:
                    chapter_num = int(m.group(1))
                    break

        if chapter_num is None:
            print(f"  page {page_idx}: 'Exercises' found but chapter undetermined — skipping")
            continue

        # Collect text: this page + up to 10 following pages
        ex_parts = []
        for idx in range(page_idx, min(page_idx + 11, total_pages)):
            t = pages_text[idx][1]
            # Stop if a different chapter starts
            if idx > page_idx:
                m = chapter_header_re.search(t)
                if m and int(m.group(1)) != chapter_num:
                    break
            ex_parts.append(t)

        combined = "\n".join(ex_parts)

        # Slice from "Exercises" heading onward
        ex_match = exercises_heading_re.search(combined)
        if not ex_match:
            continue
        ex_section = combined[ex_match.end():]

        # Parse numbered questions
        questions = []
        for qm in question_re.finditer(ex_section):
            q_text = qm.group(2).strip()
            q_text = re.sub(r'\s+', ' ', q_text)   # collapse whitespace
            q_text = re.sub(r'\s*\n\s*', ' ', q_text)
            if len(q_text) >= 20:
                questions.append(q_text)

        if questions:
            chapters[str(chapter_num)] = {
                "title": chapter_title,
                "questions": [
                    {
                        "id": f"{book_key}_ch{chapter_num}_q{j + 1}",
                        "text": q,
                        "model_answer": None,
                        "model_answer_cached_at": None,
                    }
                    for j, q in enumerate(questions)
                ],
            }
            print(f"  Ch{chapter_num} '{chapter_title[:50]}': {len(questions)} exercises")
        else:
            print(f"  Ch{chapter_num}: Exercises heading found but no numbered questions parsed")

    return chapters


def main():
    # Load existing data to preserve cached model_answers on re-run
    existing: dict = {}
    if OUTPUT.exists():
        try:
            existing = json.loads(OUTPUT.read_text(encoding="utf-8"))
        except Exception:
            pass

    output_data: dict = {}

    for book_key, (filename, label) in BOOKS_CONFIG.items():
        pdf_path = BOOKS_DIR / filename
        if not pdf_path.exists():
            print(f"WARNING: {filename} not found — skipping")
            continue

        print(f"\nExtracting exercises from {label} ...")
        chapters = extract_exercises(pdf_path, book_key)

        if not chapters:
            print(f"  No exercises found — the PDF may use image-based pages or non-standard formatting.")
            continue

        # Merge: preserve existing model_answer caches
        existing_chs = existing.get(book_key, {}).get("chapters", {})
        for ch_key, ch_data in chapters.items():
            old_qs = {q["id"]: q for q in existing_chs.get(ch_key, {}).get("questions", [])}
            for q in ch_data["questions"]:
                if q["id"] in old_qs:
                    q["model_answer"] = old_qs[q["id"]].get("model_answer")
                    q["model_answer_cached_at"] = old_qs[q["id"]].get("model_answer_cached_at")

        output_data[book_key] = {"label": label, "chapters": chapters}
        total_q = sum(len(ch["questions"]) for ch in chapters.values())
        print(f"  Done: {len(chapters)} chapters, {total_q} total exercises")

    if output_data:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps(output_data, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nSaved to {OUTPUT}")
    else:
        print("\nNo exercises extracted from any book. Check that PDFs are text-based (not scanned).")


if __name__ == "__main__":
    main()
