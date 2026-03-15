import chromadb
from pathlib import Path

CHROMA_PATH = Path(__file__).parent.parent / "data" / "chroma_db"
COLLECTION_NAME = "ml_books"

_client = None
_collection = None


def _get_collection():
    global _client, _collection
    if _collection is None:
        _client = chromadb.PersistentClient(path=str(CHROMA_PATH))
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
    return _collection


def retrieve_chunks(query: str, n_results: int = 3, source_filter: str = None) -> list[dict]:
    """Retrieve top-n relevant chunks from the books for a given query.

    Args:
        source_filter: If set, only return chunks whose 'source' metadata matches this value.
                       E.g. "Geron Hands-On ML" to restrict to Géron's book only.
    """
    collection = _get_collection()
    count = collection.count()
    if count == 0:
        return []

    n_results = min(n_results, count)
    where = {"source": {"$eq": source_filter}} if source_filter else None
    results = collection.query(
        query_texts=[query],
        n_results=n_results,
        where=where,
        include=["documents", "metadatas", "distances"],
    )

    chunks = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        chunks.append({"text": doc, "source": meta.get("source", "unknown"), "distance": dist})
    return chunks


def format_chunks_for_prompt(chunks: list[dict]) -> str:
    if not chunks:
        return "No book passages retrieved (books not yet indexed)."
    parts = []
    for i, chunk in enumerate(chunks, 1):
        parts.append(f"[Passage {i} — {chunk['source']}]\n{chunk['text']}")
    return "\n\n".join(parts)
