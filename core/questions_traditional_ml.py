# Traditional ML — Decision Trees, Ensembles, SVMs, Clustering, Dimensionality Reduction
# Covers Google interview topics: Classification, Supervised & Unsupervised Learning,
# Bayesian Models, Optimization (non-DL), Applied ML
# IDs: 501–550

TRADITIONAL_ML_QUESTIONS = [
    # ── DECISION TREES ─────────────────────────────────────────────
    {
        "id": 501,
        "text": "How does a decision tree split? Write the information gain formula using entropy. When would you use Gini impurity instead?",
        "tag": "decision_trees", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 502,
        "text": "What is pruning in decision trees? Compare pre-pruning vs post-pruning. What problem does it solve?",
        "tag": "decision_trees", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 503,
        "text": "Why do decision trees overfit? What hyperparameters control tree complexity? Give the bias-variance tradeoff for a depth-1 vs depth-20 tree.",
        "tag": "decision_trees", "difficulty": "medium", "source": "Traditional ML",
    },

    # ── RANDOM FORESTS ─────────────────────────────────────────────
    {
        "id": 504,
        "text": "What is a Random Forest? How does bagging reduce variance? Why do we also randomly subsample features at each split?",
        "tag": "random_forest", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 505,
        "text": "What is out-of-bag (OOB) error in Random Forests? How is it computed and why is it a useful estimate?",
        "tag": "random_forest", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 506,
        "text": "How does Random Forest compute feature importance? What is permutation importance and how does it differ from impurity-based importance?",
        "tag": "random_forest", "difficulty": "hard", "source": "Traditional ML",
    },

    # ── BOOSTING ───────────────────────────────────────────────────
    {
        "id": 507,
        "text": "What is the difference between bagging and boosting? How does each reduce error? Which reduces bias vs variance?",
        "tag": "ensemble", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 508,
        "text": "Explain AdaBoost. How are sample weights updated after each weak learner? Write the weight update equation.",
        "tag": "adaboost", "difficulty": "hard", "source": "Traditional ML",
    },
    {
        "id": 509,
        "text": "What is Gradient Boosting? How does it frame boosting as gradient descent in function space? Write the pseudo-residual update.",
        "tag": "gradient_boosting", "difficulty": "hard", "source": "Traditional ML",
    },
    {
        "id": 510,
        "text": "What makes XGBoost faster and more regularized than vanilla Gradient Boosting? Explain the objective function with regularization term.",
        "tag": "gradient_boosting", "difficulty": "hard", "source": "Traditional ML",
    },
    {
        "id": 511,
        "text": "What is early stopping in boosting? How do you set the number of trees? What is the role of learning rate (shrinkage)?",
        "tag": "gradient_boosting", "difficulty": "medium", "source": "Traditional ML",
    },

    # ── SUPPORT VECTOR MACHINES ────────────────────────────────────
    {
        "id": 512,
        "text": "What is a Support Vector Machine? Write the hard-margin SVM objective. What are support vectors?",
        "tag": "svm", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 513,
        "text": "What is the kernel trick in SVMs? Why does it allow non-linear classification without explicitly computing feature maps? Give 2 common kernels.",
        "tag": "svm", "difficulty": "hard", "source": "Traditional ML",
    },
    {
        "id": 514,
        "text": "What is the soft-margin SVM? Write the slack variable formulation. What does the C hyperparameter control?",
        "tag": "svm", "difficulty": "medium", "source": "Traditional ML",
    },

    # ── NAIVE BAYES & LOGISTIC REGRESSION ──────────────────────────
    {
        "id": 515,
        "text": "Logistic regression vs Naive Bayes for classification: when would you prefer each? What is the key independence assumption in Naive Bayes?",
        "tag": "classification", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 516,
        "text": "Derive the logistic regression gradient update from the log-likelihood. Why is logistic regression a linear classifier?",
        "tag": "classification", "difficulty": "hard", "source": "Traditional ML",
    },

    # ── K-NEAREST NEIGHBORS ────────────────────────────────────────
    {
        "id": 517,
        "text": "How does KNN work? What is the curse of dimensionality and why does it hurt KNN specifically? How do you choose k?",
        "tag": "knn", "difficulty": "medium", "source": "Traditional ML",
    },

    # ── CLUSTERING ─────────────────────────────────────────────────
    {
        "id": 518,
        "text": "How does K-Means work? Write the objective function. What is the inertia/WCSS? What are the limitations of K-Means?",
        "tag": "clustering", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 519,
        "text": "Compare K-Means vs DBSCAN vs Hierarchical Clustering. When would you use each? What types of clusters can each discover?",
        "tag": "clustering", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 520,
        "text": "What is the silhouette score? How do you evaluate clustering quality when you have no labels?",
        "tag": "clustering", "difficulty": "medium", "source": "Traditional ML",
    },

    # ── DIMENSIONALITY REDUCTION ───────────────────────────────────
    {
        "id": 521,
        "text": "What does PCA maximize? Derive the first principal component as an eigenvector problem. What fraction of variance does it explain?",
        "tag": "pca", "difficulty": "hard", "source": "Traditional ML",
    },
    {
        "id": 522,
        "text": "What is t-SNE? How does it differ from PCA? Why can't you use t-SNE embeddings for downstream ML tasks?",
        "tag": "dimensionality_reduction", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 523,
        "text": "What is UMAP? How does it compare to t-SNE in terms of speed, global structure preservation, and use in production?",
        "tag": "dimensionality_reduction", "difficulty": "medium", "source": "Traditional ML",
    },

    # ── BAYESIAN MODELS ────────────────────────────────────────────
    {
        "id": 524,
        "text": "What is a Gaussian Process? How does it define a distribution over functions? When would you use it over a neural network?",
        "tag": "bayesian", "difficulty": "hard", "source": "Traditional ML",
    },
    {
        "id": 525,
        "text": "What is MAP estimation vs MLE? How does adding a prior change the optimal solution? Give a concrete example with L2 regularization.",
        "tag": "bayesian", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 526,
        "text": "What is a Bayesian Network? What is conditional independence? How does the d-separation criterion work?",
        "tag": "bayesian", "difficulty": "hard", "source": "Traditional ML",
    },

    # ── EVALUATION METRICS ─────────────────────────────────────────
    {
        "id": 527,
        "text": "Explain precision, recall, F1, and AUC-ROC. When is AUC-ROC misleading? When would you prefer precision-recall curve?",
        "tag": "evaluation", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 528,
        "text": "What is the difference between macro, micro, and weighted F1? When does each matter? Give an example with class imbalance.",
        "tag": "evaluation", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 529,
        "text": "What is calibration in ML models? What is the reliability diagram (calibration curve)? When does a well-performing model have poor calibration?",
        "tag": "evaluation", "difficulty": "hard", "source": "Traditional ML",
    },

    # ── FEATURE ENGINEERING ────────────────────────────────────────
    {
        "id": 530,
        "text": "What is feature scaling? When does it matter (SVM, KNN, LR) vs when it doesn't (tree models)? Compare min-max vs z-score normalization.",
        "tag": "feature_engineering", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 531,
        "text": "How do you handle missing values? Compare imputation strategies: mean/median, model-based, multiple imputation. What are the risks of each?",
        "tag": "feature_engineering", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 532,
        "text": "What is target encoding? What is the risk of target leakage with it? How do you apply it correctly in cross-validation?",
        "tag": "feature_engineering", "difficulty": "hard", "source": "Traditional ML",
    },

    # ── CROSS-VALIDATION & MODEL SELECTION ─────────────────────────
    {
        "id": 533,
        "text": "Compare k-fold, stratified k-fold, leave-one-out, and time-series cross-validation. When does each apply?",
        "tag": "model_selection", "difficulty": "medium", "source": "Traditional ML",
    },
    {
        "id": 534,
        "text": "What is hyperparameter search? Compare grid search, random search, and Bayesian optimization. What makes Bayesian optimization more efficient?",
        "tag": "model_selection", "difficulty": "medium", "source": "Traditional ML",
    },
]
