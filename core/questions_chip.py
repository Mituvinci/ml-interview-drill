# Chip Huyen — Designing ML Systems, All 11 Chapters
# Priority from study card: hard = Must Master (data leakage, distribution shifts)

CHIP_QUESTIONS = [
    # ── CH1: ML IN PRODUCTION ──────────────────────────────────────
    {
        "id": 201,
        "text": "When should you NOT use ML to solve a problem? Give 3 concrete criteria.",
        "tag": "ml_in_production", "difficulty": "medium", "source": "Chip Ch1",
    },
    {
        "id": 202,
        "text": "What are the key differences between ML in research vs ML in production? List at least 4 dimensions.",
        "tag": "ml_in_production", "difficulty": "medium", "source": "Chip Ch1",
    },
    {
        "id": 203,
        "text": "What are the main components of an ML system in production? Draw the system diagram.",
        "tag": "ml_in_production", "difficulty": "medium", "source": "Chip Ch1",
    },

    # ── CH2: SYSTEMS DESIGN ────────────────────────────────────────
    {
        "id": 204,
        "text": "How do you frame an ML problem from a business requirement? Walk through the steps.",
        "tag": "ml_systems_design", "difficulty": "medium", "source": "Chip Ch2",
    },
    {
        "id": 205,
        "text": "What is the difference between objective functions and business metrics? Why can optimizing one hurt the other?",
        "tag": "ml_systems_design", "difficulty": "hard", "source": "Chip Ch2",
    },
    {
        "id": 206,
        "text": "What does 'mind vs data' mean in ML system design? When should you invest in more data vs better models?",
        "tag": "ml_systems_design", "difficulty": "medium", "source": "Chip Ch2",
    },

    # ── CH3: DATA ENGINEERING ──────────────────────────────────────
    {
        "id": 207,
        "text": "What are the tradeoffs between row-based vs column-based data storage formats (e.g. CSV vs Parquet)?",
        "tag": "data_engineering", "difficulty": "medium", "source": "Chip Ch3",
    },
    {
        "id": 208,
        "text": "What is ETL? How does it differ from ELT? Which is better for ML pipelines and why?",
        "tag": "data_engineering", "difficulty": "medium", "source": "Chip Ch3",
    },
    {
        "id": 209,
        "text": "What are the different types of data joins in ML? When does a join introduce data leakage?",
        "tag": "data_engineering", "difficulty": "hard", "source": "Chip Ch3",
    },

    # ── CH4: TRAINING DATA ─────────────────────────────────────────
    {
        "id": 210,
        "text": "What is the difference between random sampling and stratified sampling? When does random sampling fail for ML?",
        "tag": "training_data", "difficulty": "medium", "source": "Chip Ch4",
    },
    {
        "id": 211,
        "text": "What are the main approaches to data labeling? Compare programmatic labeling vs human labeling — tradeoffs?",
        "tag": "training_data", "difficulty": "medium", "source": "Chip Ch4",
    },
    {
        "id": 212,
        "text": "How do you handle class imbalance? Describe resampling, cost-sensitive learning, and threshold tuning — tradeoffs of each.",
        "tag": "class_imbalance", "difficulty": "medium", "source": "Chip Ch4",
    },
    {
        "id": 213,
        "text": "What is data augmentation? Give 3 examples for different data modalities. What are the risks?",
        "tag": "training_data", "difficulty": "medium", "source": "Chip Ch4",
    },

    # ── CH5: FEATURE ENGINEERING ───────────────────────────────────
    {
        "id": 214,
        "text": "What is data leakage? Define it precisely. Give 3 real-world examples from ML systems.",
        "tag": "data_leakage", "difficulty": "hard", "source": "Chip Ch5",
    },
    {
        "id": 215,
        "text": "What are the two types of data leakage: train-test leakage vs temporal leakage? How do you detect each?",
        "tag": "data_leakage", "difficulty": "hard", "source": "Chip Ch5",
    },
    {
        "id": 216,
        "text": "What feature engineering operations are commonly applied? Compare normalization vs standardization — when to use each?",
        "tag": "feature_engineering", "difficulty": "medium", "source": "Chip Ch5",
    },
    {
        "id": 217,
        "text": "What is feature importance? Name 3 methods to measure it. What are the limitations of each?",
        "tag": "feature_engineering", "difficulty": "medium", "source": "Chip Ch5",
    },

    # ── CH6: MODEL DEVELOPMENT ─────────────────────────────────────
    {
        "id": 218,
        "text": "How do you select a model for a new ML task? What criteria beyond accuracy matter in production?",
        "tag": "model_development", "difficulty": "medium", "source": "Chip Ch6",
    },
    {
        "id": 219,
        "text": "What is experiment tracking? What should you log? Why does it matter for reproducibility?",
        "tag": "model_development", "difficulty": "easy", "source": "Chip Ch6",
    },
    {
        "id": 220,
        "text": "How do you debug an ML model that is not learning? Walk through your systematic debugging process.",
        "tag": "model_development", "difficulty": "hard", "source": "Chip Ch6",
    },

    # ── CH7: DEPLOYMENT ────────────────────────────────────────────
    {
        "id": 221,
        "text": "What is the difference between batch prediction and online prediction? When do you use each?",
        "tag": "deployment", "difficulty": "medium", "source": "Chip Ch7",
    },
    {
        "id": 222,
        "text": "What is model compression? Describe quantization, pruning, and knowledge distillation.",
        "tag": "deployment", "difficulty": "hard", "source": "Chip Ch7",
    },
    {
        "id": 223,
        "text": "What does it mean to test an ML model in production? What is shadow deployment and A/B testing?",
        "tag": "deployment", "difficulty": "medium", "source": "Chip Ch7",
    },

    # ── CH8: SHIFTS & MONITORING ───────────────────────────────────
    {
        "id": 224,
        "text": "What is concept drift? What is data drift? What is covariate shift? Distinguish all three with equations.",
        "tag": "distribution_shift", "difficulty": "hard", "source": "Chip Ch8",
    },
    {
        "id": 225,
        "text": "How do you detect distribution shift in production? Name 3 statistical methods. What are their tradeoffs?",
        "tag": "distribution_shift", "difficulty": "hard", "source": "Chip Ch8",
    },
    {
        "id": 226,
        "text": "What ML system failures can occur in production beyond model degradation? Give 3 categories with examples.",
        "tag": "monitoring", "difficulty": "medium", "source": "Chip Ch8",
    },
    {
        "id": 227,
        "text": "What metrics should you monitor for an ML system in production? Distinguish operational vs ML metrics.",
        "tag": "monitoring", "difficulty": "medium", "source": "Chip Ch8",
    },

    # ── CH9: CONTINUAL LEARNING ────────────────────────────────────
    {
        "id": 228,
        "text": "What is continual learning? Why is it needed in production ML? What is catastrophic forgetting?",
        "tag": "continual_learning", "difficulty": "medium", "source": "Chip Ch9",
    },
    {
        "id": 229,
        "text": "What is the difference between stateless and stateful retraining? When would you use each?",
        "tag": "continual_learning", "difficulty": "medium", "source": "Chip Ch9",
    },

    # ── CH10-11: INFRASTRUCTURE & HUMAN SIDE ──────────────────────
    {
        "id": 230,
        "text": "What is an ML platform? What are its key components? How does it differ from a data platform?",
        "tag": "ml_infrastructure", "difficulty": "medium", "source": "Chip Ch10",
    },
    {
        "id": 231,
        "text": "What does responsible AI mean in practice? Name 3 failure modes and how to address them.",
        "tag": "responsible_ai", "difficulty": "medium", "source": "Chip Ch11",
    },
]
