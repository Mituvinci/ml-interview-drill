// DrillMenuScreen + TOPIC_GROUPS
const { useState, useEffect } = React;

const TOPIC_GROUPS = [
  { label: "Linear Algebra", color: "blue", topics: [
    { tag: "linear_regression", label: "Linear Regression" },
    { tag: "svd", label: "SVD" },
    { tag: "svd_pca", label: "SVD & PCA" },
    { tag: "eigendecomposition", label: "Eigendecomposition" },
    { tag: "norms", label: "Norms" },
    { tag: "linear_algebra_basics", label: "LA Basics" },
    { tag: "matrix_multiplication", label: "Matrix Multiply" },
  ]},
  { label: "Optimization", color: "orange", topics: [
    { tag: "gradient_descent", label: "Gradient Descent" },
    { tag: "adam_optimizer", label: "Adam Optimizer" },
    { tag: "vanishing_gradient", label: "Vanishing Gradient" },
    { tag: "exploding_gradient", label: "Exploding Gradient" },
  ]},
  { label: "Deep Learning", color: "purple", topics: [
    { tag: "backprop", label: "Backpropagation" },
    { tag: "attention", label: "Attention / Transformers" },
    { tag: "batch_norm", label: "Batch Normalization" },
    { tag: "dropout", label: "Dropout" },
    { tag: "cnn", label: "CNNs & ResNets" },
    { tag: "normalization", label: "Normalization Techniques" },
    { tag: "autoencoders", label: "Autoencoders" },
    { tag: "vae", label: "VAEs" },
    { tag: "lstm", label: "LSTM / GRU" },
  ]},
  { label: "Probability & Stats", color: "green", topics: [
    { tag: "bayes", label: "Bayes Theorem" },
    { tag: "mle", label: "MLE" },
    { tag: "bias_variance", label: "Bias-Variance" },
    { tag: "cross_entropy", label: "Cross-Entropy" },
    { tag: "bayesian", label: "Bayesian Models" },
    { tag: "evaluation", label: "Eval Metrics" },
  ]},
  { label: "Regularization", color: "yellow", topics: [
    { tag: "regularization", label: "L1 / L2 Regularization" },
  ]},
  { label: "Traditional ML", color: "teal", topics: [
    { tag: "decision_trees", label: "Decision Trees" },
    { tag: "random_forest", label: "Random Forest" },
    { tag: "ensemble", label: "Bagging vs Boosting" },
    { tag: "adaboost", label: "AdaBoost" },
    { tag: "gradient_boosting", label: "Gradient Boosting / XGBoost" },
    { tag: "svm", label: "SVMs" },
    { tag: "classification", label: "Logistic Reg / Naive Bayes" },
    { tag: "knn", label: "KNN" },
    { tag: "clustering", label: "Clustering" },
    { tag: "pca", label: "PCA" },
    { tag: "dimensionality_reduction", label: "t-SNE / UMAP" },
    { tag: "feature_engineering", label: "Feature Engineering" },
    { tag: "model_selection", label: "Cross-Validation" },
  ]},
  { label: "ML Systems", color: "red", topics: [
    { tag: "data_leakage", label: "Data Leakage" },
    { tag: "class_imbalance", label: "Class Imbalance" },
    { tag: "concept_drift", label: "Concept Drift" },
    { tag: "time_series", label: "Time Series" },
    { tag: "health_ai", label: "Health AI" },
    { tag: "bioinformatics", label: "Bioinformatics / Genomics" },
  ]},
  { label: "LLM & Agents", color: "indigo", topics: [
    { tag: "llm_fundamentals", label: "LLM Fundamentals" },
    { tag: "agent_architecture", label: "Agent Architecture" },
    { tag: "tool_use", label: "Tool Use" },
    { tag: "agent_memory", label: "Memory Types" },
    { tag: "rag", label: "RAG" },
    { tag: "multi_agent", label: "Multi-Agent" },
    { tag: "prompt_engineering", label: "Prompt Engineering" },
    { tag: "tokenization", label: "Tokenization" },
    { tag: "llm_finetuning", label: "Fine-tuning / LoRA / RLHF" },
    { tag: "foundation_models", label: "Foundation Models" },
    { tag: "in_context_learning", label: "In-Context Learning" },
    { tag: "llm_reasoning", label: "LLM Reasoning" },
  ]},
  { label: "Transfer & Few-Shot", color: "pink", topics: [
    { tag: "transfer_learning", label: "Transfer Learning" },
    { tag: "few_shot", label: "Few-Shot Learning" },
    { tag: "explainability", label: "Explainability (SHAP/LIME)" },
  ]},
];

function DrillMenuScreen({ onBack, onRandom, onDrillTag }) {
  const [progress, setProgress] = useState(null);

  useEffect(() => {
    apiFetch("/api/progress").then(setProgress).catch(() => {});
  }, []);

  const scoreColor = (tag) => {
    if (!progress) return "";
    const s = progress.weak_spots?.[tag] || progress.all_topics?.[tag];
    if (!s) return "bg-gray-100 text-gray-700 hover:bg-gray-200";
    if (s.score_avg < 4) return "bg-red-100 text-red-800 hover:bg-red-200";
    if (s.score_avg < 6) return "bg-yellow-100 text-yellow-800 hover:bg-yellow-200";
    return "bg-green-100 text-green-800 hover:bg-green-200";
  };

  const scoreLabel = (tag) => {
    if (!progress) return null;
    const s = progress.weak_spots?.[tag] || progress.all_topics?.[tag];
    if (!s || !s.attempts) return null;
    return `${s.score_avg.toFixed(1)}`;
  };

  const groupBorder = {
    blue:"border-blue-200", orange:"border-orange-200", purple:"border-purple-200",
    green:"border-green-200", yellow:"border-yellow-200", red:"border-red-200",
    indigo:"border-indigo-200", teal:"border-teal-200", pink:"border-pink-200",
  };
  const groupHeader = {
    blue:"text-blue-700", orange:"text-orange-700", purple:"text-purple-700",
    green:"text-green-700", yellow:"text-yellow-700", red:"text-red-700",
    indigo:"text-indigo-700", teal:"text-teal-700", pink:"text-pink-700",
  };

  return (
    <div className="max-w-3xl mx-auto p-4 pb-16 fade-in">
      <div className="flex items-center gap-4 mb-6">
        <Btn onClick={onBack} variant="secondary">← Back</Btn>
        <div>
          <h1 className="text-2xl font-bold text-indigo-600">Core Drill</h1>
          <p className="text-sm text-gray-500">Choose a mode — scores show your current average</p>
        </div>
      </div>

      <div className="mb-6 p-4 bg-indigo-50 border border-indigo-200 rounded-xl">
        <div className="flex items-center justify-between">
          <div>
            <h2 className="font-bold text-indigo-700 text-lg">Random Drill</h2>
            <p className="text-sm text-gray-500 mt-1">Mix of all topics — 70% from your weak spots, 30% random</p>
          </div>
          <Btn onClick={onRandom} className="px-6 py-3 text-lg">Start →</Btn>
        </div>
      </div>

      <h2 className="font-bold text-gray-700 mb-3 text-lg">Drill by Topic</h2>
      <div className="space-y-4">
        {TOPIC_GROUPS.map(group => (
          <div key={group.label} className={`border ${groupBorder[group.color]} rounded-xl p-3`}>
            <h3 className={`font-bold text-sm uppercase tracking-wide mb-2 ${groupHeader[group.color]}`}>{group.label}</h3>
            <div className="flex flex-wrap gap-2">
              {group.topics.map(t => {
                const avg = scoreLabel(t.tag);
                return (
                  <button key={t.tag} onClick={() => onDrillTag(t.tag)}
                    className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors ${scoreColor(t.tag)}`}>
                    {t.label}
                    {avg && <span className="ml-1.5 text-xs opacity-70">({avg})</span>}
                  </button>
                );
              })}
            </div>
          </div>
        ))}
      </div>

      <p className="text-xs text-gray-400 mt-4 text-center">
        Green ≥ 6.0 · Yellow 4–6 · Red &lt; 4 · Gray = not attempted
      </p>
    </div>
  );
}
