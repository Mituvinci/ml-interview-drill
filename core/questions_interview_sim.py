"""
Interview Simulation Questions — IDs 901–940
These are Zoom-interview style: conceptual, comparison, explanation.
No "derive from scratch" — real interviewers ask why, what, when, how it differs.
"""

INTERVIEW_SIM_QUESTIONS = [
    # ── Optimization ────────────────────────────────────────────────────────
    {
        "id": 901,
        "text": (
            "What is the Adam optimizer and how does it differ from SGD and RMSProp? "
            "In plain terms, what two things does Adam track and why does that help?"
        ),
        "tag": "adam_optimizer",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 902,
        "text": (
            "When would you choose Adam over vanilla SGD? "
            "Are there any situations where SGD is actually better than Adam?"
        ),
        "tag": "adam_optimizer",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 903,
        "text": (
            "What is the vanishing gradient problem? "
            "Give me two practical ways to deal with it in a deep neural network."
        ),
        "tag": "vanishing_gradient",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 904,
        "text": (
            "What is gradient clipping and why do you need it? "
            "In which type of models does exploding gradients most commonly occur?"
        ),
        "tag": "exploding_gradient",
        "difficulty": "easy",
        "source": "Interview Sim",
    },

    # ── Linear Algebra & Regression ─────────────────────────────────────────
    {
        "id": 910,
        "text": (
            "How does a system of linear equations like 3x + 4y + 4z = 10 become the matrix form "
            "Xw = y used in linear regression? Walk me through what X, w, and y represent."
        ),
        "tag": "linear_regression",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 911,
        "text": (
            "What is SVD and why is it useful in machine learning? "
            "Can you give one practical example of where you'd use it?"
        ),
        "tag": "svd",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 912,
        "text": (
            "What is PCA and how does it relate to SVD? "
            "When would you use PCA before training a model?"
        ),
        "tag": "pca",
        "difficulty": "medium",
        "source": "Interview Sim",
    },

    # ── Regularization ───────────────────────────────────────────────────────
    {
        "id": 920,
        "text": (
            "What is the difference between L1 and L2 regularization? "
            "When would you prefer L1 over L2?"
        ),
        "tag": "regularization",
        "difficulty": "easy",
        "source": "Interview Sim",
    },
    {
        "id": 921,
        "text": (
            "What is dropout and how does it prevent overfitting? "
            "Does it behave the same way at training time and inference time?"
        ),
        "tag": "dropout",
        "difficulty": "easy",
        "source": "Interview Sim",
    },

    # ── Deep Learning ────────────────────────────────────────────────────────
    {
        "id": 930,
        "text": (
            "What is the attention mechanism and why did it replace RNNs for sequence tasks? "
            "What key problem with RNNs does attention solve?"
        ),
        "tag": "attention",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 931,
        "text": (
            "What is batch normalization and why does it help training? "
            "Does batch norm behave differently at train vs inference time?"
        ),
        "tag": "batch_norm",
        "difficulty": "easy",
        "source": "Interview Sim",
    },
    {
        "id": 932,
        "text": (
            "What is backpropagation at a high level? "
            "If a layer has zero gradient, what does that mean and what might cause it?"
        ),
        "tag": "backprop",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 933,
        "text": (
            "What is a residual connection (skip connection) in ResNets? "
            "What problem in deep networks does it solve?"
        ),
        "tag": "cnn",
        "difficulty": "easy",
        "source": "Interview Sim",
    },

    # ── Traditional ML ───────────────────────────────────────────────────────
    {
        "id": 940,
        "text": (
            "What is the difference between bagging and boosting? "
            "Give one example algorithm for each."
        ),
        "tag": "ensemble",
        "difficulty": "easy",
        "source": "Interview Sim",
    },
    {
        "id": 941,
        "text": (
            "How does XGBoost differ from a standard random forest? "
            "What makes gradient boosting powerful?"
        ),
        "tag": "gradient_boosting",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 942,
        "text": (
            "What is an SVM? What does the kernel trick do and why is it useful?"
        ),
        "tag": "svm",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 943,
        "text": (
            "How do you handle class imbalance in a classification problem? "
            "Name at least three approaches and when you'd use each."
        ),
        "tag": "class_imbalance",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 944,
        "text": (
            "What is data leakage? Give a concrete real-world example where it would silently "
            "inflate your validation accuracy."
        ),
        "tag": "data_leakage",
        "difficulty": "medium",
        "source": "Interview Sim",
    },

    # ── Probability & Stats ───────────────────────────────────────────────────
    {
        "id": 950,
        "text": (
            "What is the bias-variance tradeoff? "
            "If your model has high training accuracy but poor validation accuracy, "
            "what does that tell you?"
        ),
        "tag": "bias_variance",
        "difficulty": "easy",
        "source": "Interview Sim",
    },
    {
        "id": 951,
        "text": (
            "What is the difference between precision and recall? "
            "Give an example of when you'd prioritize recall over precision."
        ),
        "tag": "evaluation",
        "difficulty": "easy",
        "source": "Interview Sim",
    },
    {
        "id": 952,
        "text": (
            "What does ROC-AUC measure and what does an AUC of 0.5 mean? "
            "When is ROC-AUC a misleading metric?"
        ),
        "tag": "evaluation",
        "difficulty": "medium",
        "source": "Interview Sim",
    },

    # ── LLM & Agents ─────────────────────────────────────────────────────────
    {
        "id": 960,
        "text": (
            "What is LoRA and why is it used for fine-tuning large language models? "
            "What does it save compared to full fine-tuning?"
        ),
        "tag": "llm_finetuning",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
    {
        "id": 961,
        "text": (
            "What is RAG (Retrieval-Augmented Generation)? "
            "What problem does it solve that plain fine-tuning doesn't?"
        ),
        "tag": "rag",
        "difficulty": "easy",
        "source": "Interview Sim",
    },
    {
        "id": 962,
        "text": (
            "What is RLHF and what problem does it solve in LLM training? "
            "What are the main steps in the RLHF pipeline?"
        ),
        "tag": "llm_finetuning",
        "difficulty": "medium",
        "source": "Interview Sim",
    },
]
