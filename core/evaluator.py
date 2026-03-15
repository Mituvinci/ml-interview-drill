import json
import anthropic
from core.rag import retrieve_chunks, format_chunks_for_prompt

MODEL = "claude-sonnet-4-20250514"

EVALUATOR_SYSTEM_PROMPT = """
You are a rigorous ML technical interviewer evaluating a PhD candidate
applying for ML Engineer / Research Scientist roles at top tech companies.

The candidate is strong in applied ML and bioinformatics but has identified
weaknesses in mathematical articulation under pressure.

Your job: evaluate their answer to the question with the following criteria:
1. Mathematical correctness (equations, notation, derivations)
2. Conceptual completeness (are key ideas present?)
3. Clarity (could they explain this in an interview?)
4. Depth (do they understand WHY, not just WHAT?)

Use the provided book passages as ground truth. If the candidate's answer
matches the book's explanation, score higher. If it contradicts it, flag it.

Be direct and specific. Do not be encouraging for wrong answers.
Point out exactly what equation or concept is missing.

When explaining equations, always use LaTeX notation wrapped in $...$ for inline
and $$...$$ for block equations. For example:
- Inline: The update rule is $\theta = \theta - \alpha \nabla J(\theta)$
- Block: $$A = U \Sigma V^T$$
Always write matrices and equations in LaTeX. Never use plain text like X^T or ||g||.

For book_reference: ALWAYS include the author's name and book title. Use the
source label from the passage header. Example: "From Goodfellow et al. Deep Learning, Ch.6: ..."
or "From Géron Hands-On ML: ..." or "From Chip Huyen Designing ML Systems: ..."

For improved_answer and what_is_missing: use Markdown formatting.
Use **bold** for key terms, bullet lists for multiple points, and LaTeX for equations.

Return ONLY valid JSON matching the schema. No markdown wrapper, no preamble.
"""

EVAL_SCHEMA = """{
  "score": <0-10>,
  "verdict": "<correct | partial | incorrect>",
  "what_you_got_right": "<string with markdown>",
  "what_is_missing": "<string with markdown>",
  "book_reference": "<From [Author] [Book Title]: exact quote or summary>",
  "improved_answer": "<string with markdown and LaTeX>",
  "follow_up_question": "<string>",
  "topic_tag": "<tag string>"
}"""


def evaluate_answer(question_text: str, user_answer: str, topic_tag: str) -> dict:
    chunks = retrieve_chunks(query=f"{question_text} {topic_tag}", n_results=3)
    book_context = format_chunks_for_prompt(chunks)

    user_prompt = f"""Question: {question_text}

Candidate's Answer:
{user_answer}

Relevant Book Passages:
{book_context}

Evaluate the candidate's answer and return JSON matching this schema:
{EVAL_SCHEMA}"""

    client = anthropic.Anthropic()
    message = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        temperature=0,
        system=EVALUATOR_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = message.content[0].text.strip()
    # Strip markdown code fences if model wraps output
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)
