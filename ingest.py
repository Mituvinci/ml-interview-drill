"""
PDF + Markdown ingestion script: reads books from data/books/ and indexes into ChromaDB.
Run once before starting the app:  uv run python ingest.py
"""
import re
import sys
from pathlib import Path
import fitz  # PyMuPDF
import chromadb

BOOKS_DIR = Path(__file__).parent / "data" / "books"
CHROMA_PATH = Path(__file__).parent / "data" / "chroma_db"
COLLECTION_NAME = "ml_books"
CHUNK_SIZE = 800
CHUNK_OVERLAP = 100

# Named PDF books with explicit labels
BOOK_FILES = {
    "goodfellow.pdf": "Goodfellow Deep Learning",
    "chip_huyen.pdf": "Chip Huyen Designing ML Systems",
    "geron.pdf": "Geron Hands-On ML",
}

# Markdown directories: dir_path (relative to BOOKS_DIR) -> source label
MARKDOWN_DIRS = {
    "ml-interviews-book-master/contents": "Chip Huyen ML Interviews",
    "ml-interviews-book-master/answers":  "Chip Huyen ML Interviews Answers",
    "ed_donner_slides_md":                "Ed Donner Agentic AI",
}

# Markdown files to skip (noise / stubs / metadata)
SKIP_MD_FILES = {
    "README.md", "study-notes.md", "resources.md", "ToC.md",
    "SUMMARY.md", "book.json", "0-about-the-author.md", "0-acknowledgments.md",
}

# Individual markdown files in the root of BOOKS_DIR (not in a subdirectory)
# Add your own .md files here: "filename.md": "Source Label"
SINGLE_MD_FILES = {}

# Folders to scan recursively for PDFs (agentic AI slides etc.)
EXTRA_DIRS = {
    "agentic_ai_slides": "Agentic AI Slides",
}

# Files to always skip
SKIP_FILES = {".env", ".env.example"}


def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP) -> list[str]:
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def clean_markdown(text: str) -> str:
    """Strip Markdown/HTML formatting, keep plain readable text."""
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove image refs ![alt](url)
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    # Convert links [text](url) -> text
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    # Remove reference-style links [^n]: ...
    text = re.sub(r'^\[\^[^\]]+\]:.*$', '', text, flags=re.MULTILINE)
    # Remove horizontal rules
    text = re.sub(r'^[-*_]{3,}\s*$', '', text, flags=re.MULTILINE)
    # Remove code fences (keep content)
    text = re.sub(r'```[a-z]*\n', '', text)
    text = text.replace('```', '')
    # Collapse multiple blank lines
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def ingest_markdown_dir(dir_path: Path, source_label: str, collection) -> int:
    """Ingest all .md files in a directory into ChromaDB. Returns chunk count."""
    md_files = sorted(dir_path.glob("*.md"))
    md_files = [f for f in md_files if f.name not in SKIP_MD_FILES]

    if not md_files:
        print(f"    No .md files found in {dir_path.name}/")
        return 0

    all_chunks, ids, metadatas = [], [], []

    for md_path in md_files:
        raw = md_path.read_text(encoding="utf-8", errors="ignore")
        text = clean_markdown(raw)
        if len(text.strip()) < 50:   # skip near-empty stubs
            continue
        for i, chunk in enumerate(chunk_text(text)):
            chunk_id = f"md_{md_path.stem[:40]}_c{i}"
            all_chunks.append(chunk)
            ids.append(chunk_id)
            metadatas.append({"source": source_label, "page": 0, "file": md_path.name})

    if all_chunks:
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            collection.upsert(
                documents=all_chunks[i: i + batch_size],
                ids=ids[i: i + batch_size],
                metadatas=metadatas[i: i + batch_size],
            )

    return len(all_chunks)


def ingest_pdf(pdf_path: Path, source_label: str, collection) -> int:
    doc = fitz.open(str(pdf_path))
    all_chunks = []
    ids = []
    metadatas = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        if not text.strip():
            continue
        for i, chunk in enumerate(chunk_text(text)):
            chunk_id = f"{pdf_path.stem}_p{page_num}_c{i}"
            all_chunks.append(chunk)
            ids.append(chunk_id)
            metadatas.append({"source": source_label, "page": page_num, "file": pdf_path.name})

    if all_chunks:
        batch_size = 100
        for i in range(0, len(all_chunks), batch_size):
            collection.upsert(
                documents=all_chunks[i: i + batch_size],
                ids=ids[i: i + batch_size],
                metadatas=metadatas[i: i + batch_size],
            )

    doc.close()
    return len(all_chunks)


def main():
    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    collection = client.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    total = 0
    found_any = False

    # Ingest named books
    for filename, label in BOOK_FILES.items():
        pdf_path = BOOKS_DIR / filename
        if not pdf_path.exists():
            print(f"  WARNING: {filename} not found — skipping.")
            continue
        print(f"  Indexing {filename} ...")
        n = ingest_pdf(pdf_path, label, collection)
        print(f"    -> {n} chunks")
        total += n
        found_any = True

    # Ingest Markdown books
    for rel_dir, label in MARKDOWN_DIRS.items():
        md_dir = BOOKS_DIR / rel_dir
        if not md_dir.exists():
            print(f"  WARNING: {rel_dir}/ not found — skipping.")
            continue
        print(f"  Indexing Markdown from {rel_dir}/ ...")
        n = ingest_markdown_dir(md_dir, label, collection)
        if n > 0:
            print(f"    -> {n} chunks")
            total += n
            found_any = True
        else:
            print(f"    -> No usable text found")

    # Ingest individual markdown files
    for filename, label in SINGLE_MD_FILES.items():
        md_path = BOOKS_DIR / filename
        if not md_path.exists():
            print(f"  WARNING: {filename} not found — skipping.")
            continue
        print(f"  Indexing {filename} ...")
        raw = md_path.read_text(encoding="utf-8", errors="ignore")
        text = clean_markdown(raw)
        chunks = chunk_text(text)
        ids = [f"md_{md_path.stem[:40]}_c{i}" for i in range(len(chunks))]
        metadatas = [{"source": label, "page": 0, "file": filename} for _ in chunks]
        for i in range(0, len(chunks), 100):
            collection.upsert(documents=chunks[i:i+100], ids=ids[i:i+100], metadatas=metadatas[i:i+100])
        print(f"    -> {len(chunks)} chunks")
        total += len(chunks)
        found_any = True

    # Ingest extra directories (agentic AI slides etc.)
    for dir_name, label in EXTRA_DIRS.items():
        extra_dir = BOOKS_DIR / dir_name
        if not extra_dir.exists():
            print(f"  WARNING: {dir_name}/ not found — skipping.")
            continue
        pdfs = sorted(extra_dir.glob("**/*.pdf"))
        if not pdfs:
            print(f"  WARNING: No PDFs found in {dir_name}/")
            continue
        print(f"  Indexing {len(pdfs)} PDFs from {dir_name}/ ...")
        dir_total = 0
        image_only = 0
        for pdf_path in pdfs:
            if pdf_path.name in SKIP_FILES:
                continue
            n = ingest_pdf(pdf_path, label, collection)
            if n == 0:
                image_only += 1
            dir_total += n
        print(f"    -> {dir_total} chunks ({image_only} image-only PDFs skipped)")
        if dir_total > 0:
            found_any = True
            total += dir_total
        else:
            print(f"    NOTE: All slides in {dir_name}/ are image-based — no text extracted.")
            print(f"          RAG will not have context for agentic AI questions.")
            print(f"          Claude will still evaluate answers from its own knowledge.")

    if not found_any:
        print("\nNo content found to index. Check that books exist in data/books/.")
        sys.exit(1)

    print(f"\nDone. Total chunks indexed: {total}")
    print(f"ChromaDB collection '{COLLECTION_NAME}' now has {collection.count()} documents.")


if __name__ == "__main__":
    main()
