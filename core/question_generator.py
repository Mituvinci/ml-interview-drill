"""
Dynamic question generator — ALL drill questions come from here.
Generates interview-style questions via Claude API + RAG.
Caches to data/generated_questions.json so each question is generated once.
"""
import json
import random
from datetime import datetime
from pathlib import Path
import anthropic
from core.rag import retrieve_chunks, format_chunks_for_prompt

MODEL = "claude-sonnet-4-20250514"
GENERATED_FILE = Path(__file__).parent.parent / "data" / "generated_questions.json"
GENERATED_ID_START = 10000  # generated questions start at 10001

# Fallback topic pool used when user has no weak spots yet
FALLBACK_TAGS = [
    "linear_regression", "svd", "gradient_descent", "adam_optimizer",
    "backprop", "attention", "batch_norm", "dropout", "regularization",
    "bias_variance", "cross_entropy", "decision_trees", "random_forest",
    "gradient_boosting", "svm", "clustering", "pca", "llm_fundamentals",
    "rag", "llm_finetuning", "data_leakage", "class_imbalance",
    "vanishing_gradient", "svd_pca", "evaluation", "feature_engineering",
]

SYSTEM_PROMPT = """You are a senior ML interviewer at a top tech company screening a PhD candidate \
for a Machine Learning Engineer or Research Scientist role.

Your job is to generate ONE interview question about a specific ML topic.

Rules for the question:
- Ask it exactly the way a real interviewer would say it on a Zoom call
- Conceptual, comparison, or "explain the intuition" style
- Good examples:
    "What is Adam and how does it differ from SGD? When would you choose one over the other?"
    "What is dropout and why does it only apply at training time, not inference?"
    "How does a random forest reduce variance compared to a single decision tree?"
    "What problem does batch normalization solve and where in the network do you apply it?"
- NEVER ask the candidate to derive an equation from scratch
- NEVER use "prove that", "derive", "write the full derivation of"
- Equations are allowed ONLY to clarify the question, not as the main task
- Assume the candidate has a PhD in CS/ML — test whether they can explain clearly
  under interview pressure, not whether they can do math on a whiteboard
- One question only. No sub-questions. No bullet lists. Just the question as spoken.

Return ONLY valid JSON, no markdown, no preamble:
{
  "text": "the question exactly as the interviewer would ask it",
  "tag": "<topic_tag>",
  "difficulty": "medium",
  "hint": "one sentence that nudges without giving the answer away"
}"""

USER_PROMPT = """Topic: {topic}

Relevant passages from the candidate's study books:
{book_context}

Questions already generated for this topic (do NOT repeat or paraphrase these):
{seen_questions}

Generate one new interview question about: {topic}"""


def _load() -> list:
    if GENERATED_FILE.exists():
        return json.loads(GENERATED_FILE.read_text(encoding="utf-8"))
    return []


def _save(questions: list):
    GENERATED_FILE.parent.mkdir(parents=True, exist_ok=True)
    GENERATED_FILE.write_text(json.dumps(questions, indent=2, ensure_ascii=False), encoding="utf-8")


def get_generated_question(question_id: int) -> dict | None:
    for q in _load():
        if q["id"] == question_id:
            return q
    return None


def get_cached_for_tag(tag: str) -> list:
    return [q for q in _load() if q["tag"] == tag]


def pick_topic_from_progress(progress: dict) -> str:
    """Pick a topic to drill: 70% weak spots, 30% random fallback."""
    weak_spots = progress.get("weak_spots", {})
    weak_tags = [t for t, s in weak_spots.items() if s.get("score_avg", 10) < 6.0]
    all_attempted_tags = list(weak_spots.keys())

    if weak_tags and random.random() < 0.70:
        return random.choice(weak_tags)
    if all_attempted_tags:
        return random.choice(all_attempted_tags)
    return random.choice(FALLBACK_TAGS)


def serve_or_generate(tag: str, progress: dict) -> dict:
    """
    Main entry point for the drill endpoint.
    Returns a cached unanswered question for this tag, or generates a new one.
    """
    cached = get_cached_for_tag(tag)
    attempted_ids = {s["question_id"] for s in progress.get("sessions", [])}

    # Find a cached question the user hasn't answered yet
    unanswered = [q for q in cached if q["id"] not in attempted_ids]
    if unanswered:
        return random.choice(unanswered)

    # Nothing unanswered — generate a fresh one
    return _generate(tag, cached)


def _generate(topic: str, existing_for_tag: list) -> dict:
    """Call Claude to generate one new interview question for this topic."""
    # RAG: pull relevant book passages for this topic
    chunks = retrieve_chunks(query=topic.replace("_", " "), n_results=3)
    book_context = format_chunks_for_prompt(chunks) if chunks else "No passages found for this topic."

    # Build the "already seen" block to avoid repeats
    seen_texts = [q["text"] for q in existing_for_tag[-20:]]
    seen_block = "\n".join(f"- {t[:120]}" for t in seen_texts) if seen_texts else "None yet."

    user_msg = USER_PROMPT.format(
        topic=topic,
        book_context=book_context,
        seen_questions=seen_block,
    )

    client = anthropic.Anthropic()
    msg = client.messages.create(
        model=MODEL,
        max_tokens=512,
        temperature=0.8,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_msg}],
    )
    raw = msg.content[0].text.strip()
    # Strip markdown fences if model adds them
    if raw.startswith("```"):
        raw = raw.split("```", 1)[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.rsplit("```", 1)[0]

    q_data = json.loads(raw.strip())

    all_generated = _load()
    question = {
        "id": GENERATED_ID_START + 1 + len(all_generated),
        "text": q_data["text"],
        "tag": q_data.get("tag", topic),
        "difficulty": q_data.get("difficulty", "medium"),
        "hint": q_data.get("hint", ""),
        "source": "Generated",
        "generated_at": datetime.utcnow().isoformat(),
    }
    all_generated.append(question)
    _save(all_generated)
    return question
