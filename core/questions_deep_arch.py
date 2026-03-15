# Deep Learning Architecture & Advanced ML
# Covers Google interview topics: Autoencoders/VAEs, Transfer Learning, LSTM/GRU,
# Time Series, Explainability (XAI/SHAP/LIME), Tokenization, Few-shot Learning,
# LLM Fine-tuning, Foundation Models, In-context Learning, LLM Reasoning
# IDs: 601–650

DEEP_ARCH_QUESTIONS = [
    # ── AUTOENCODERS & VAEs ────────────────────────────────────────
    {
        "id": 601,
        "text": "What is an autoencoder? What is the bottleneck and why does it force useful representations? How is it used in anomaly detection?",
        "tag": "autoencoders", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 602,
        "text": "What is a Variational Autoencoder (VAE)? Write the ELBO objective. What does the KL divergence term enforce?",
        "tag": "vae", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 603,
        "text": "What is the reparameterization trick in VAEs? Why is it necessary for backpropagation through a stochastic layer?",
        "tag": "vae", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 604,
        "text": "Compare VAE vs GAN: what does each optimize? What are the failure modes (posterior collapse, mode collapse)?",
        "tag": "vae", "difficulty": "hard", "source": "Deep Arch",
    },

    # ── RECURRENT NETWORKS & TIME SERIES ──────────────────────────
    {
        "id": 605,
        "text": "What is an LSTM? Write the forget, input, and output gate equations. How does it solve the vanishing gradient problem of vanilla RNNs?",
        "tag": "lstm", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 606,
        "text": "What is a GRU? How does it differ from an LSTM? What are the tradeoffs in expressiveness vs computational cost?",
        "tag": "lstm", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 607,
        "text": "What is time series forecasting? Compare autoregressive models (AR/ARIMA), RNN-based, and Transformer-based approaches. When does each shine?",
        "tag": "time_series", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 608,
        "text": "What is temporal data leakage? Give 3 concrete examples. How do you correctly split train/val/test for time series?",
        "tag": "time_series", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 609,
        "text": "What is stationarity in time series? How do you test for it (ADF test)? How do you make a non-stationary series stationary?",
        "tag": "time_series", "difficulty": "medium", "source": "Deep Arch",
    },

    # ── TRANSFER LEARNING ─────────────────────────────────────────
    {
        "id": 610,
        "text": "What is transfer learning? Explain feature extraction vs fine-tuning. When does each strategy work better?",
        "tag": "transfer_learning", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 611,
        "text": "What is domain adaptation? How does covariate shift differ from label shift? What techniques address each?",
        "tag": "transfer_learning", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 612,
        "text": "What is cross-modal transfer learning? Give an example of knowledge transferring between modalities (e.g. text→image, image→genomics).",
        "tag": "transfer_learning", "difficulty": "hard", "source": "Deep Arch",
    },

    # ── FEW-SHOT LEARNING ─────────────────────────────────────────
    {
        "id": 613,
        "text": "What is few-shot learning? Compare meta-learning (MAML), metric learning (Prototypical Networks), and in-context learning for few-shot tasks.",
        "tag": "few_shot", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 614,
        "text": "What is Prototypical Networks? How are class prototypes computed and how is inference done? Write the distance-based classification formula.",
        "tag": "few_shot", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 615,
        "text": "What is MAML (Model-Agnostic Meta-Learning)? Explain the bi-level optimization objective. What is the computational bottleneck?",
        "tag": "few_shot", "difficulty": "hard", "source": "Deep Arch",
    },

    # ── TOKENIZATION ──────────────────────────────────────────────
    {
        "id": 616,
        "text": "What is Byte-Pair Encoding (BPE)? Walk through the algorithm step-by-step. Why do LLMs use subword tokenization instead of word or character tokenization?",
        "tag": "tokenization", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 617,
        "text": "What is WordPiece tokenization (BERT)? How does it differ from BPE? What is SentencePiece and when is it used?",
        "tag": "tokenization", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 618,
        "text": "How does tokenization affect model performance on math, code, and non-English languages? Why do some languages get 'penalized' by tokenization?",
        "tag": "tokenization", "difficulty": "medium", "source": "Deep Arch",
    },

    # ── EXPLAINABILITY (XAI) ───────────────────────────────────────
    {
        "id": 619,
        "text": "What is SHAP? Explain Shapley values from cooperative game theory. Why are they considered the 'fairest' feature attribution method?",
        "tag": "explainability", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 620,
        "text": "What is LIME? How does it approximate local model behavior? Compare to SHAP in terms of consistency and computational cost.",
        "tag": "explainability", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 621,
        "text": "What is a saliency map in neural networks? Compare gradient-based (vanilla, integrated gradients) vs attention-based explanations.",
        "tag": "explainability", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 622,
        "text": "What is Grad-CAM? How does it use gradients flowing into the final convolutional layer to produce a localization map?",
        "tag": "explainability", "difficulty": "medium", "source": "Deep Arch",
    },

    # ── LLM FINE-TUNING ───────────────────────────────────────────
    {
        "id": 623,
        "text": "What is LoRA (Low-Rank Adaptation)? Write the weight update decomposition. Why does it dramatically reduce the number of trainable parameters?",
        "tag": "llm_finetuning", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 624,
        "text": "What is RLHF (Reinforcement Learning from Human Feedback)? Walk through the 3 stages: SFT, reward model training, PPO fine-tuning.",
        "tag": "llm_finetuning", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 625,
        "text": "What is DPO (Direct Preference Optimization)? How does it achieve alignment without a separate reward model? Write the loss function.",
        "tag": "llm_finetuning", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 626,
        "text": "What is catastrophic forgetting? How does it affect LLM fine-tuning? What techniques mitigate it (EWC, replay, LoRA, etc.)?",
        "tag": "llm_finetuning", "difficulty": "hard", "source": "Deep Arch",
    },

    # ── FOUNDATION MODELS & IN-CONTEXT LEARNING ───────────────────
    {
        "id": 627,
        "text": "What is in-context learning (ICL)? Why can transformers learn from examples in the context window without gradient updates? What is the proposed mechanistic explanation?",
        "tag": "in_context_learning", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 628,
        "text": "What is chain-of-thought (CoT) prompting? Why does asking a model to 'think step by step' improve reasoning performance?",
        "tag": "llm_reasoning", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 629,
        "text": "What is scaling law for LLMs (Chinchilla)? Write the compute-optimal relationship between model size, dataset size, and FLOPs.",
        "tag": "foundation_models", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 630,
        "text": "What is emergent capability in foundation models? Give 3 examples. Why is emergence controversial and hard to predict?",
        "tag": "foundation_models", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 631,
        "text": "What is instruction tuning? How does FLAN differ from GPT-3? Why does instruction tuning improve zero-shot generalization?",
        "tag": "llm_finetuning", "difficulty": "medium", "source": "Deep Arch",
    },

    # ── LLM REASONING ─────────────────────────────────────────────
    {
        "id": 632,
        "text": "What is the difference between System 1 and System 2 thinking in LLMs? How do test-time compute methods (tree-of-thought, MCTS) relate to this?",
        "tag": "llm_reasoning", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 633,
        "text": "What is hallucination in LLMs? What are the root causes? What mitigation strategies exist (RAG, RLHF, self-consistency)?",
        "tag": "llm_reasoning", "difficulty": "medium", "source": "Deep Arch",
    },

    # ── CONVOLUTIONAL NETWORKS ────────────────────────────────────
    {
        "id": 634,
        "text": "Write the convolution operation for a 2D feature map. What do stride and padding do? Why does weight sharing reduce parameters?",
        "tag": "cnn", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 635,
        "text": "What is a residual connection (skip connection)? Write the ResNet block equation. Why does it solve the degradation problem in very deep networks?",
        "tag": "cnn", "difficulty": "medium", "source": "Deep Arch",
    },

    # ── NORMALIZATION TECHNIQUES ──────────────────────────────────
    {
        "id": 636,
        "text": "Compare Batch Norm, Layer Norm, Group Norm, and Instance Norm. Which axis does each normalize over? Why does LayerNorm work better in transformers?",
        "tag": "normalization", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 637,
        "text": "What is spectral normalization? Where is it used and why (GANs, Lipschitz constraints)?",
        "tag": "normalization", "difficulty": "hard", "source": "Deep Arch",
    },

    # ── BIOINFORMATICS / HEALTH AI ────────────────────────────────
    {
        "id": 638,
        "text": "How is ML applied in genomics? Compare sequence-based models (CNNs, transformers) to traditional GWAS. What is the target prediction task in gene expression?",
        "tag": "bioinformatics", "difficulty": "hard", "source": "Deep Arch",
    },
    {
        "id": 639,
        "text": "What are the unique challenges of healthcare ML? Address: class imbalance, distribution shift across hospitals, interpretability requirements, and regulatory constraints.",
        "tag": "health_ai", "difficulty": "medium", "source": "Deep Arch",
    },
    {
        "id": 640,
        "text": "What is federated learning? How does it preserve data privacy for healthcare ML? What are its limitations compared to centralized training?",
        "tag": "health_ai", "difficulty": "hard", "source": "Deep Arch",
    },
]
