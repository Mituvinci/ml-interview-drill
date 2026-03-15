# Géron — Hands-On ML, Selected Chapters
# Ch2 (E2E Project), Ch3 (Classification), Ch4 (Training Models),
# Ch5 (SVMs), Ch8 (Dim Reduction), Ch10 (Neural Nets),
# Ch11 (Training Deep Nets), Ch15 (RNNs), Ch17 (Autoencoders/GANs)

GERON_QUESTIONS = [

    # ── CH2: END-TO-END ML PROJECT (10 questions) ──────────────────
    {
        "id": 301,
        "text": "Walk through all the steps of an end-to-end ML project in order. What is the most commonly skipped step that causes production failures?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 302,
        "text": "What is data snooping bias? How do you create a proper test set to avoid it?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 303,
        "text": "What is stratified sampling? When is it critical vs random sampling? Give a concrete ML example.",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 304,
        "text": "What is a Scikit-Learn transformation pipeline? Why use it instead of manual preprocessing? What leakage does it prevent?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 305,
        "text": "How do you handle missing values in a dataset? Compare deletion, imputation with mean/median, and model-based imputation.",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 306,
        "text": "What is feature scaling? Compare min-max normalization vs standardization. When does each fail?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 307,
        "text": "How do you encode categorical variables? Compare one-hot encoding vs ordinal encoding — when does each cause problems?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 308,
        "text": "What is cross-validation? Write the k-fold CV procedure. How is it used for model selection without touching the test set?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 309,
        "text": "What is grid search vs randomized search for hyperparameter tuning? When do you prefer each?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },
    {
        "id": 310,
        "text": "After selecting your best model, what steps do you take before deploying it? What does Géron say about analyzing errors?",
        "tag": "e2e_ml_project", "difficulty": "medium", "source": "Géron Ch2",
    },

    # ── CH3: CLASSIFICATION (9 questions) ─────────────────────────
    {
        "id": 311,
        "text": "Why is accuracy a misleading metric for imbalanced classification? Give a numerical example where 99% accuracy is useless.",
        "tag": "classification_metrics", "difficulty": "medium", "source": "Géron Ch3",
    },
    {
        "id": 312,
        "text": "Define precision and recall. Write the formulas. What is the precision-recall tradeoff?",
        "tag": "classification_metrics", "difficulty": "medium", "source": "Géron Ch3",
    },
    {
        "id": 313,
        "text": "What is the F1 score? Write the formula. When do you use F1 vs precision vs recall alone?",
        "tag": "classification_metrics", "difficulty": "medium", "source": "Géron Ch3",
    },
    {
        "id": 314,
        "text": "What is the precision-recall curve? How do you choose the decision threshold from it?",
        "tag": "classification_metrics", "difficulty": "medium", "source": "Géron Ch3",
    },
    {
        "id": 315,
        "text": "What is the ROC curve? What does AUC measure? When do you prefer the PR curve over ROC?",
        "tag": "classification_metrics", "difficulty": "medium", "source": "Géron Ch3",
    },
    {
        "id": 316,
        "text": "What is a confusion matrix? Label all 4 cells (TP, FP, FN, TN). How do you read it for a multiclass problem?",
        "tag": "classification_metrics", "difficulty": "easy", "source": "Géron Ch3",
    },
    {
        "id": 317,
        "text": "What is multilabel classification? Give an ML example. How does it differ from multiclass classification?",
        "tag": "classification_metrics", "difficulty": "medium", "source": "Géron Ch3",
    },
    {
        "id": 318,
        "text": "What are OvR and OvO strategies for multiclass classification? When does Scikit-Learn use each?",
        "tag": "classification_metrics", "difficulty": "medium", "source": "Géron Ch3",
    },
    {
        "id": 319,
        "text": "What is the SGDClassifier? What loss functions does it support? How does it handle large datasets?",
        "tag": "classification_metrics", "difficulty": "easy", "source": "Géron Ch3",
    },

    # ── CH4: TRAINING MODELS (10 questions) ───────────────────────
    {
        "id": 320,
        "text": "Derive the normal equation θ = (XᵀX)⁻¹Xᵀy from the MSE cost function. What is its computational complexity?",
        "tag": "training_models", "difficulty": "hard", "source": "Géron Ch4",
    },
    {
        "id": 321,
        "text": "Write the MSE cost function for linear regression. Take the gradient and set it to zero to derive the normal equation.",
        "tag": "training_models", "difficulty": "hard", "source": "Géron Ch4",
    },
    {
        "id": 322,
        "text": "Compare batch GD, stochastic GD, and mini-batch GD. Write the update rules. What are the convergence properties of each?",
        "tag": "training_models", "difficulty": "hard", "source": "Géron Ch4",
    },
    {
        "id": 323,
        "text": "What is a learning schedule? What is learning rate decay? Why does SGD need it but batch GD does not?",
        "tag": "training_models", "difficulty": "medium", "source": "Géron Ch4",
    },
    {
        "id": 324,
        "text": "What is polynomial regression? How do you add polynomial features? How does the degree affect bias and variance?",
        "tag": "training_models", "difficulty": "medium", "source": "Géron Ch4",
    },
    {
        "id": 325,
        "text": "Write the Ridge regression cost function. How does λ control the bias-variance tradeoff? What happens as λ → ∞?",
        "tag": "regularization", "difficulty": "hard", "source": "Géron Ch4",
    },
    {
        "id": 326,
        "text": "Write the Lasso cost function. Why does it produce sparse solutions? What happens to small weights?",
        "tag": "regularization", "difficulty": "hard", "source": "Géron Ch4",
    },
    {
        "id": 327,
        "text": "What is Elastic Net? Write the cost function. When do you use it instead of Ridge or Lasso?",
        "tag": "regularization", "difficulty": "medium", "source": "Géron Ch4",
    },
    {
        "id": 328,
        "text": "What is early stopping regularization? How do you implement it? Why does it work?",
        "tag": "regularization", "difficulty": "medium", "source": "Géron Ch4",
    },
    {
        "id": 329,
        "text": "Derive the logistic regression cost function from maximum likelihood. Why use log-loss instead of MSE for classification?",
        "tag": "logistic_regression", "difficulty": "hard", "source": "Géron Ch4",
    },
    {
        "id": 330,
        "text": "What is the softmax function? Write the equation. How is it used in multiclass logistic regression?",
        "tag": "logistic_regression", "difficulty": "medium", "source": "Géron Ch4",
    },

    # ── CH5: SVMs (8 questions) ────────────────────────────────────
    {
        "id": 331,
        "text": "What is a support vector machine? What is the margin? What are support vectors? Draw the decision boundary.",
        "tag": "svm", "difficulty": "medium", "source": "Géron Ch5",
    },
    {
        "id": 332,
        "text": "What is hard margin vs soft margin SVM? What is the C hyperparameter? How does it control the bias-variance tradeoff?",
        "tag": "svm", "difficulty": "hard", "source": "Géron Ch5",
    },
    {
        "id": 333,
        "text": "Write the SVM optimization objective (primal form). What does maximizing the margin mean mathematically?",
        "tag": "svm", "difficulty": "hard", "source": "Géron Ch5",
    },
    {
        "id": 334,
        "text": "What is the kernel trick? Why does it avoid explicit feature mapping? Write the kernel function definition.",
        "tag": "svm", "difficulty": "hard", "source": "Géron Ch5",
    },
    {
        "id": 335,
        "text": "Write the RBF (Gaussian) kernel. What does γ control? What happens when γ is too large or too small?",
        "tag": "svm", "difficulty": "hard", "source": "Géron Ch5",
    },
    {
        "id": 336,
        "text": "Compare polynomial kernel vs RBF kernel. When would you choose each for a classification problem?",
        "tag": "svm", "difficulty": "medium", "source": "Géron Ch5",
    },
    {
        "id": 337,
        "text": "Can SVMs be used for regression? What is SVR? How does the ε-tube work?",
        "tag": "svm", "difficulty": "medium", "source": "Géron Ch5",
    },
    {
        "id": 338,
        "text": "What are the computational limitations of SVMs for large datasets? How does LinearSVC differ from SVC?",
        "tag": "svm", "difficulty": "medium", "source": "Géron Ch5",
    },

    # ── CH8: DIMENSIONALITY REDUCTION (8 questions) ───────────────
    {
        "id": 339,
        "text": "What is the curse of dimensionality? How does it affect distance metrics and density estimation?",
        "tag": "dimensionality_reduction", "difficulty": "medium", "source": "Géron Ch8",
    },
    {
        "id": 340,
        "text": "What is the projection approach to dimensionality reduction? When does it fail (give an example like Swiss roll)?",
        "tag": "dimensionality_reduction", "difficulty": "medium", "source": "Géron Ch8",
    },
    {
        "id": 341,
        "text": "Walk through PCA step by step. How do you compute principal components using SVD? Write the projection equation.",
        "tag": "pca", "difficulty": "hard", "source": "Géron Ch8",
    },
    {
        "id": 342,
        "text": "How do you choose the number of principal components? What is the explained variance ratio? Write the formula.",
        "tag": "pca", "difficulty": "medium", "source": "Géron Ch8",
    },
    {
        "id": 343,
        "text": "What is randomized PCA vs incremental PCA? When do you use each for large datasets?",
        "tag": "pca", "difficulty": "medium", "source": "Géron Ch8",
    },
    {
        "id": 344,
        "text": "What is kernel PCA? How does it enable non-linear dimensionality reduction? What kernel would you choose for a circular dataset?",
        "tag": "pca", "difficulty": "hard", "source": "Géron Ch8",
    },
    {
        "id": 345,
        "text": "What is t-SNE? How does it differ from PCA? When do you use t-SNE vs PCA?",
        "tag": "dimensionality_reduction", "difficulty": "medium", "source": "Géron Ch8",
    },
    {
        "id": 346,
        "text": "What is LLE (Locally Linear Embedding)? What manifold assumption does it make? What are its limitations?",
        "tag": "dimensionality_reduction", "difficulty": "medium", "source": "Géron Ch8",
    },

    # ── CH10: NEURAL NETS (9 questions) ───────────────────────────
    {
        "id": 347,
        "text": "What is a perceptron? Write the output equation. What is its fundamental limitation and how does MLP solve it?",
        "tag": "neural_nets", "difficulty": "medium", "source": "Géron Ch10",
    },
    {
        "id": 348,
        "text": "What is a multilayer perceptron (MLP)? What is the universal approximation theorem?",
        "tag": "neural_nets", "difficulty": "medium", "source": "Géron Ch10",
    },
    {
        "id": 349,
        "text": "Compare sigmoid, tanh, and ReLU activations. Write equations and derivatives. What is the dying ReLU problem?",
        "tag": "neural_nets", "difficulty": "hard", "source": "Géron Ch10",
    },
    {
        "id": 350,
        "text": "What is Leaky ReLU? Write the equation. How does it fix the dying ReLU problem?",
        "tag": "neural_nets", "difficulty": "medium", "source": "Géron Ch10",
    },
    {
        "id": 351,
        "text": "How many layers and neurons should you use? What are the rules of thumb for architecture selection?",
        "tag": "neural_nets", "difficulty": "medium", "source": "Géron Ch10",
    },
    {
        "id": 352,
        "text": "What loss function do you use for binary classification, multiclass classification, and regression in neural nets?",
        "tag": "neural_nets", "difficulty": "easy", "source": "Géron Ch10",
    },
    {
        "id": 353,
        "text": "What is backpropagation? Write the chain rule for a weight in the second-to-last layer.",
        "tag": "backprop", "difficulty": "hard", "source": "Géron Ch10",
    },
    {
        "id": 354,
        "text": "What is the role of the learning rate in neural network training? What happens if it is too high or too low?",
        "tag": "neural_nets", "difficulty": "medium", "source": "Géron Ch10",
    },
    {
        "id": 355,
        "text": "What is the difference between a regression MLP and a classification MLP in terms of output layer and loss?",
        "tag": "neural_nets", "difficulty": "easy", "source": "Géron Ch10",
    },

    # ── CH11: TRAINING DEEP NETS (10 questions) ────────────────────
    {
        "id": 356,
        "text": "What is the vanishing gradient problem in deep networks? Why does it happen with sigmoid/tanh? What is the mathematical reason?",
        "tag": "vanishing_gradient", "difficulty": "hard", "source": "Géron Ch11",
    },
    {
        "id": 357,
        "text": "What is Xavier (Glorot) initialization? Write the formula. What problem does it solve?",
        "tag": "weight_initialization", "difficulty": "hard", "source": "Géron Ch11",
    },
    {
        "id": 358,
        "text": "What is He initialization? Write the formula. Why is it used with ReLU instead of Xavier?",
        "tag": "weight_initialization", "difficulty": "hard", "source": "Géron Ch11",
    },
    {
        "id": 359,
        "text": "What is batch normalization? Write the normalization and scale/shift equations. Where is it placed in the network?",
        "tag": "batch_norm", "difficulty": "hard", "source": "Géron Ch11",
    },
    {
        "id": 360,
        "text": "Write the Adam optimizer update equations including bias correction. Why is bias correction needed?",
        "tag": "adam_optimizer", "difficulty": "hard", "source": "Géron Ch11",
    },
    {
        "id": 361,
        "text": "What is RMSProp? Write the update rule. What problem does it solve that momentum SGD does not?",
        "tag": "adam_optimizer", "difficulty": "hard", "source": "Géron Ch11",
    },
    {
        "id": 362,
        "text": "What is dropout? Write the training vs inference behavior mathematically. What is the inverted dropout trick?",
        "tag": "dropout", "difficulty": "medium", "source": "Géron Ch11",
    },
    {
        "id": 363,
        "text": "What is Monte Carlo dropout? How is it used for uncertainty estimation at inference time?",
        "tag": "dropout", "difficulty": "hard", "source": "Géron Ch11",
    },
    {
        "id": 364,
        "text": "What is transfer learning? When does it work well? What layers do you freeze vs fine-tune?",
        "tag": "transfer_learning", "difficulty": "medium", "source": "Géron Ch11",
    },
    {
        "id": 365,
        "text": "What is learning rate scheduling? Compare step decay, exponential decay, and cosine annealing.",
        "tag": "training_models", "difficulty": "medium", "source": "Géron Ch11",
    },

    # ── CH15: RNNs (8 questions) ───────────────────────────────────
    {
        "id": 366,
        "text": "What is a recurrent neural network? Write the hidden state update equation h_t = f(W_hh·h_{t-1} + W_xh·x_t + b).",
        "tag": "rnn", "difficulty": "hard", "source": "Géron Ch15",
    },
    {
        "id": 367,
        "text": "What is backpropagation through time (BPTT)? Why does it cause vanishing/exploding gradients in RNNs?",
        "tag": "rnn", "difficulty": "hard", "source": "Géron Ch15",
    },
    {
        "id": 368,
        "text": "What is an LSTM? Draw all 4 gates: forget, input, gate, output. Write the equations for each gate.",
        "tag": "lstm", "difficulty": "hard", "source": "Géron Ch15",
    },
    {
        "id": 369,
        "text": "What is a GRU? How does it differ from LSTM? Write the update and reset gate equations.",
        "tag": "lstm", "difficulty": "hard", "source": "Géron Ch15",
    },
    {
        "id": 370,
        "text": "What is a sequence-to-sequence model? What is the encoder-decoder architecture? Where is attention added?",
        "tag": "rnn", "difficulty": "hard", "source": "Géron Ch15",
    },
    {
        "id": 371,
        "text": "What is teacher forcing in RNN training? What is exposure bias and how does it affect production?",
        "tag": "rnn", "difficulty": "medium", "source": "Géron Ch15",
    },
    {
        "id": 372,
        "text": "What is a 1D convolutional layer for sequence data? How does it compare to RNNs for time series?",
        "tag": "rnn", "difficulty": "medium", "source": "Géron Ch15",
    },
    {
        "id": 373,
        "text": "What are the main use cases for RNNs vs Transformers for sequence modeling today? When would you still use an LSTM?",
        "tag": "rnn", "difficulty": "medium", "source": "Géron Ch15",
    },

    # ── CH17: AUTOENCODERS & GANs (9 questions) ───────────────────
    {
        "id": 374,
        "text": "What is an autoencoder? What is the encoder, bottleneck, and decoder? Write the reconstruction loss.",
        "tag": "autoencoders", "difficulty": "medium", "source": "Géron Ch17",
    },
    {
        "id": 375,
        "text": "What is an undercomplete autoencoder? What does it learn in the bottleneck? How is it related to PCA?",
        "tag": "autoencoders", "difficulty": "medium", "source": "Géron Ch17",
    },
    {
        "id": 376,
        "text": "What is a denoising autoencoder? How is noise added during training? What does it force the model to learn?",
        "tag": "autoencoders", "difficulty": "medium", "source": "Géron Ch17",
    },
    {
        "id": 377,
        "text": "How is an autoencoder used for anomaly detection? What threshold do you use and how do you set it?",
        "tag": "autoencoders", "difficulty": "medium", "source": "Géron Ch17",
    },
    {
        "id": 378,
        "text": "What is a Variational Autoencoder (VAE)? Write the ELBO loss = reconstruction loss + KL divergence. What does each term do?",
        "tag": "autoencoders", "difficulty": "hard", "source": "Géron Ch17",
    },
    {
        "id": 379,
        "text": "What is the reparameterization trick in VAEs? Why is it needed for backpropagation through a stochastic layer?",
        "tag": "autoencoders", "difficulty": "hard", "source": "Géron Ch17",
    },
    {
        "id": 380,
        "text": "What is a GAN? Write the minimax objective: min_G max_D V(D,G). What does each player optimize?",
        "tag": "gans", "difficulty": "hard", "source": "Géron Ch17",
    },
    {
        "id": 381,
        "text": "What is mode collapse in GANs? Why does it happen? Name 3 techniques to address it.",
        "tag": "gans", "difficulty": "hard", "source": "Géron Ch17",
    },
    {
        "id": 382,
        "text": "What is a conditional GAN (cGAN)? How does conditioning work? What is it used for?",
        "tag": "gans", "difficulty": "medium", "source": "Géron Ch17",
    },
]
