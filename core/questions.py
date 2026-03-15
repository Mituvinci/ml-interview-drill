from typing import TypedDict
from core.questions_goodfellow import GOODFELLOW_QUESTIONS
from core.questions_chip import CHIP_QUESTIONS
from core.questions_geron import GERON_QUESTIONS
from core.questions_agentic import AGENTIC_QUESTIONS
from core.questions_traditional_ml import TRADITIONAL_ML_QUESTIONS
from core.questions_deep_arch import DEEP_ARCH_QUESTIONS
from core.questions_interview_sim import INTERVIEW_SIM_QUESTIONS


class Question(TypedDict):
    id: int
    text: str
    tag: str
    difficulty: str
    source: str


# Original 25 core questions
CORE_QUESTIONS: list[Question] = [
    {
        "id": 1, "source": "Core",
        "text": "Write the closed-form solution for linear regression. Derive it from scratch.",
        "tag": "linear_regression", "difficulty": "medium",
    },
    {
        "id": 2, "source": "Core",
        "text": "What is SVD? Write A = UΣVᵀ and explain each component.",
        "tag": "svd", "difficulty": "hard",
    },
    {
        "id": 3, "source": "Core",
        "text": "How is SVD related to PCA? Walk through the connection mathematically.",
        "tag": "svd_pca", "difficulty": "hard",
    },
    {
        "id": 4, "source": "Core",
        "text": "What is an eigendecomposition? When does it exist?",
        "tag": "eigendecomposition", "difficulty": "medium",
    },
    {
        "id": 5, "source": "Core",
        "text": "Why is (XᵀX)⁻¹ sometimes numerically unstable? What do you do about it?",
        "tag": "linear_regression", "difficulty": "hard",
    },
    {
        "id": 6, "source": "Core",
        "text": "Write the gradient descent update rule. What does each term mean?",
        "tag": "gradient_descent", "difficulty": "easy",
    },
    {
        "id": 7, "source": "Core",
        "text": "What is the vanishing gradient problem? Why does it happen mathematically?",
        "tag": "vanishing_gradient", "difficulty": "medium",
    },
    {
        "id": 8, "source": "Core",
        "text": "What is the exploding gradient problem? How do you fix it?",
        "tag": "exploding_gradient", "difficulty": "medium",
    },
    {
        "id": 9, "source": "Core",
        "text": "Derive the Adam optimizer update rule. What problem does it solve over SGD?",
        "tag": "adam_optimizer", "difficulty": "hard",
    },
    {
        "id": 10, "source": "Core",
        "text": "What is gradient clipping? Write the equation. When do you use it?",
        "tag": "exploding_gradient", "difficulty": "medium",
    },
    {
        "id": 11, "source": "Core",
        "text": "Write L1 and L2 regularization loss functions. What is the geometric difference?",
        "tag": "regularization", "difficulty": "medium",
    },
    {
        "id": 12, "source": "Core",
        "text": "Why does L1 produce sparse weights? Explain with the gradient.",
        "tag": "regularization", "difficulty": "hard",
    },
    {
        "id": 13, "source": "Core",
        "text": "What is dropout? How does it work at training vs inference time?",
        "tag": "dropout", "difficulty": "medium",
    },
    {
        "id": 14, "source": "Core",
        "text": "What is weight decay? How does it relate to L2 regularization?",
        "tag": "regularization", "difficulty": "medium",
    },
    {
        "id": 15, "source": "Core",
        "text": "Write Bayes' theorem. How is it used in Naive Bayes?",
        "tag": "bayes", "difficulty": "easy",
    },
    {
        "id": 16, "source": "Core",
        "text": "What is MLE? Write the log-likelihood for a Gaussian.",
        "tag": "mle", "difficulty": "medium",
    },
    {
        "id": 17, "source": "Core",
        "text": "What is the bias-variance tradeoff? Write the decomposition.",
        "tag": "bias_variance", "difficulty": "medium",
    },
    {
        "id": 18, "source": "Core",
        "text": "What is cross-entropy loss? Derive it from MLE.",
        "tag": "cross_entropy", "difficulty": "hard",
    },
    {
        "id": 19, "source": "Core",
        "text": "Explain backpropagation using the chain rule. Write the update for one weight.",
        "tag": "backprop", "difficulty": "medium",
    },
    {
        "id": 20, "source": "Core",
        "text": "What is batch normalization? Write the equations. Why does it help?",
        "tag": "batch_norm", "difficulty": "medium",
    },
    {
        "id": 21, "source": "Core",
        "text": "What is the attention mechanism? Write the scaled dot-product attention equation.",
        "tag": "attention", "difficulty": "hard",
    },
    {
        "id": 22, "source": "Core",
        "text": "Why do transformers use scaled dot-product? What happens without scaling?",
        "tag": "attention", "difficulty": "medium",
    },
    {
        "id": 23, "source": "Core",
        "text": "What is data leakage? Give 3 examples from real ML systems.",
        "tag": "data_leakage", "difficulty": "medium",
    },
    {
        "id": 24, "source": "Core",
        "text": "How do you handle class imbalance? What are the tradeoffs of each approach?",
        "tag": "class_imbalance", "difficulty": "medium",
    },
    {
        "id": 25, "source": "Core",
        "text": "What is concept drift? How do you detect and handle it in production?",
        "tag": "concept_drift", "difficulty": "medium",
    },
]

QUESTIONS: list[Question] = (
    CORE_QUESTIONS
    + GOODFELLOW_QUESTIONS
    + CHIP_QUESTIONS
    + GERON_QUESTIONS
    + AGENTIC_QUESTIONS
    + TRADITIONAL_ML_QUESTIONS
    + DEEP_ARCH_QUESTIONS
    + INTERVIEW_SIM_QUESTIONS
)

QUESTION_MAP = {q["id"]: q for q in QUESTIONS}

# Source groups for filtered drilling
SOURCE_GROUPS = {
    "Core": [q for q in QUESTIONS if q.get("source", "").startswith("Core")],
    "Goodfellow": [q for q in QUESTIONS if q.get("source", "").startswith("Goodfellow")],
    "Chip Huyen": [q for q in QUESTIONS if q.get("source", "").startswith("Chip")],
    "Géron": [q for q in QUESTIONS if q.get("source", "").startswith("Géron")],
    "Agentic AI": [q for q in QUESTIONS if q.get("source", "").startswith("Agentic")],
    "Traditional ML": [q for q in QUESTIONS if q.get("source", "").startswith("Traditional")],
    "Deep Arch": [q for q in QUESTIONS if q.get("source", "").startswith("Deep")],
    "Interview Sim": [q for q in QUESTIONS if q.get("source", "").startswith("Interview")],
}


def get_question(question_id: int) -> Question | None:
    return QUESTION_MAP.get(question_id)


def get_all_questions() -> list[Question]:
    return QUESTIONS


def get_questions_by_source(source: str) -> list[Question]:
    return SOURCE_GROUPS.get(source, [])


def get_questions_by_tag(tag: str) -> list[Question]:
    return [q for q in QUESTIONS if q["tag"] == tag]
