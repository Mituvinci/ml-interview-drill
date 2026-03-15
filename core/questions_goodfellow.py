# Goodfellow Deep Learning — Chapter 2-5
# Priority from study card: hard = Must Master, medium = Very Important, easy = Important

GOODFELLOW_QUESTIONS = [
    # ── CHAPTER 2: LINEAR ALGEBRA ──────────────────────────────────
    {
        "id": 101,
        "text": "What is the difference between a scalar, vector, matrix, and tensor? Give the notation for each.",
        "tag": "linear_algebra_basics", "difficulty": "easy", "source": "Goodfellow Ch2",
    },
    {
        "id": 102,
        "text": "Write the rules for matrix multiplication. When is AB = BA? When does it fail?",
        "tag": "matrix_multiplication", "difficulty": "medium", "source": "Goodfellow Ch2",
    },
    {
        "id": 103,
        "text": "What is a matrix inverse? Write AA⁻¹ = I. When does the inverse not exist?",
        "tag": "matrix_inverse", "difficulty": "medium", "source": "Goodfellow Ch2",
    },
    {
        "id": 104,
        "text": "What is linear dependence? What does it mean for a set of vectors to be linearly independent?",
        "tag": "linear_dependence", "difficulty": "medium", "source": "Goodfellow Ch2",
    },
    {
        "id": 105,
        "text": "Define L¹, L², and L∞ norms. Write the equations. When do you use each in ML?",
        "tag": "norms", "difficulty": "medium", "source": "Goodfellow Ch2",
    },
    {
        "id": 106,
        "text": "What are orthogonal matrices? Write the property. Why are they computationally useful?",
        "tag": "special_matrices", "difficulty": "medium", "source": "Goodfellow Ch2",
    },
    {
        "id": 107,
        "text": "What is eigendecomposition? Write A = VΛV⁻¹. When does it exist? What do eigenvalues tell you about a matrix?",
        "tag": "eigendecomposition", "difficulty": "hard", "source": "Goodfellow Ch2",
    },
    {
        "id": 108,
        "text": "What is SVD? Write A = UΣVᵀ. How do U, Σ, V relate to eigendecomposition of AᵀA?",
        "tag": "svd", "difficulty": "hard", "source": "Goodfellow Ch2",
    },
    {
        "id": 109,
        "text": "What is the Moore-Penrose pseudoinverse? Write A⁺. When is it used instead of A⁻¹?",
        "tag": "pseudoinverse", "difficulty": "hard", "source": "Goodfellow Ch2",
    },
    {
        "id": 110,
        "text": "What is the trace of a matrix? Write Tr(A). What useful properties does it have?",
        "tag": "trace_determinant", "difficulty": "easy", "source": "Goodfellow Ch2",
    },
    {
        "id": 111,
        "text": "What is the determinant? What does det(A) = 0 mean geometrically and for solvability?",
        "tag": "trace_determinant", "difficulty": "medium", "source": "Goodfellow Ch2",
    },
    {
        "id": 112,
        "text": "Explain PCA from scratch using SVD. How do you choose the number of components? What is the reconstruction error?",
        "tag": "pca", "difficulty": "hard", "source": "Goodfellow Ch2",
    },

    # ── CHAPTER 3: PROBABILITY ─────────────────────────────────────
    {
        "id": 113,
        "text": "Why does ML use probability instead of deterministic rules? Give two concrete reasons.",
        "tag": "probability_basics", "difficulty": "easy", "source": "Goodfellow Ch3",
    },
    {
        "id": 114,
        "text": "What is the difference between a discrete and continuous random variable? How does probability mass function differ from probability density function?",
        "tag": "probability_basics", "difficulty": "easy", "source": "Goodfellow Ch3",
    },
    {
        "id": 115,
        "text": "Write the marginal probability formula. Derive P(x) from the joint P(x,y).",
        "tag": "marginal_probability", "difficulty": "medium", "source": "Goodfellow Ch3",
    },
    {
        "id": 116,
        "text": "Write the definition of conditional probability P(y|x). How does it differ from the joint P(x,y)?",
        "tag": "conditional_probability", "difficulty": "easy", "source": "Goodfellow Ch3",
    },
    {
        "id": 117,
        "text": "Write the chain rule of probability for P(x¹, x², ..., xⁿ). Give an example with 3 variables.",
        "tag": "chain_rule_probability", "difficulty": "medium", "source": "Goodfellow Ch3",
    },
    {
        "id": 118,
        "text": "What does it mean for two variables to be independent? Write the condition. What is conditional independence?",
        "tag": "independence", "difficulty": "medium", "source": "Goodfellow Ch3",
    },
    {
        "id": 119,
        "text": "Write the formulas for expectation and variance. What is covariance? What does a covariance matrix encode?",
        "tag": "expectation_variance", "difficulty": "medium", "source": "Goodfellow Ch3",
    },
    {
        "id": 120,
        "text": "Write the Bernoulli distribution PMF. What parameter controls it? Where is it used in ML?",
        "tag": "common_distributions", "difficulty": "easy", "source": "Goodfellow Ch3",
    },
    {
        "id": 121,
        "text": "Write the Gaussian (Normal) distribution PDF. What are μ and σ? Why is the Gaussian so common in ML?",
        "tag": "common_distributions", "difficulty": "medium", "source": "Goodfellow Ch3",
    },
    {
        "id": 122,
        "text": "Write the sigmoid function. Write the softplus function. What are their derivatives? Where are they used?",
        "tag": "common_functions", "difficulty": "medium", "source": "Goodfellow Ch3",
    },
    {
        "id": 123,
        "text": "Write Bayes' theorem. Identify the prior, likelihood, and posterior. Show how it applies to Naive Bayes classification.",
        "tag": "bayes", "difficulty": "hard", "source": "Goodfellow Ch3",
    },
    {
        "id": 124,
        "text": "What is entropy? Write H(x). What is KL divergence? Write D_KL(P||Q). Why is KL divergence not symmetric?",
        "tag": "information_theory", "difficulty": "hard", "source": "Goodfellow Ch3",
    },
    {
        "id": 125,
        "text": "What is cross-entropy? Write H(P,Q). How does it relate to KL divergence and why is it used as a loss function?",
        "tag": "cross_entropy", "difficulty": "hard", "source": "Goodfellow Ch3",
    },

    # ── CHAPTER 4: COMPUTATION ─────────────────────────────────────
    {
        "id": 126,
        "text": "What is numerical overflow and underflow? Give an example with softmax. How do you fix it?",
        "tag": "numerical_computation", "difficulty": "medium", "source": "Goodfellow Ch4",
    },
    {
        "id": 127,
        "text": "What is poor conditioning? What is the condition number of a matrix? Why does it cause problems in optimization?",
        "tag": "numerical_computation", "difficulty": "medium", "source": "Goodfellow Ch4",
    },
    {
        "id": 128,
        "text": "Write the gradient descent update rule. What is the learning rate? What happens if it's too large or too small?",
        "tag": "gradient_descent", "difficulty": "hard", "source": "Goodfellow Ch4",
    },
    {
        "id": 129,
        "text": "What is the difference between batch gradient descent, SGD, and mini-batch? What are the tradeoffs?",
        "tag": "gradient_descent", "difficulty": "hard", "source": "Goodfellow Ch4",
    },
    {
        "id": 130,
        "text": "What is momentum in gradient descent? Write the update rule. How does it help escape local minima?",
        "tag": "gradient_descent", "difficulty": "hard", "source": "Goodfellow Ch4",
    },

    # ── CHAPTER 5: ML BASICS ───────────────────────────────────────
    {
        "id": 131,
        "text": "What is the difference between a learning algorithm and a fixed algorithm? Define the task T, performance P, experience E framework.",
        "tag": "ml_basics", "difficulty": "easy", "source": "Goodfellow Ch5",
    },
    {
        "id": 132,
        "text": "What is overfitting and underfitting? Draw the bias-variance tradeoff curve. What controls each?",
        "tag": "overfitting_underfitting", "difficulty": "hard", "source": "Goodfellow Ch5",
    },
    {
        "id": 133,
        "text": "Write the bias-variance decomposition of MSE. Define each term mathematically.",
        "tag": "bias_variance", "difficulty": "hard", "source": "Goodfellow Ch5",
    },
    {
        "id": 134,
        "text": "What is a validation set? How does it differ from a test set? Why can't you use the test set to tune hyperparameters?",
        "tag": "validation", "difficulty": "medium", "source": "Goodfellow Ch5",
    },
    {
        "id": 135,
        "text": "What is a point estimator? Define bias and consistency of an estimator. Write the formula for estimator bias.",
        "tag": "estimators", "difficulty": "medium", "source": "Goodfellow Ch5",
    },
    {
        "id": 136,
        "text": "What is Maximum Likelihood Estimation? Write the MLE objective. Derive the MLE estimate for a Gaussian mean.",
        "tag": "mle", "difficulty": "hard", "source": "Goodfellow Ch5",
    },
    {
        "id": 137,
        "text": "What is Bayesian statistics? What is a prior, posterior, and likelihood? How does MAP differ from MLE?",
        "tag": "bayesian_statistics", "difficulty": "hard", "source": "Goodfellow Ch5",
    },
    {
        "id": 138,
        "text": "Compare logistic regression vs SVM vs k-NN for classification. When would you choose each?",
        "tag": "supervised_learning", "difficulty": "medium", "source": "Goodfellow Ch5",
    },
    {
        "id": 139,
        "text": "What is SGD? Write the update rule. Why does noise in SGD sometimes help generalization?",
        "tag": "sgd", "difficulty": "hard", "source": "Goodfellow Ch5",
    },
    {
        "id": 140,
        "text": "What are the key challenges in deep learning listed by Goodfellow? Name at least 4 and explain one in depth.",
        "tag": "dl_challenges", "difficulty": "medium", "source": "Goodfellow Ch5",
    },
]
