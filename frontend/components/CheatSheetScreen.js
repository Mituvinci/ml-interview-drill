// CheatSheetScreen
const { useState, useEffect, useRef } = React;

function CheatSheetScreen({ onBack, onDrillTag }) {
  const [tab, setTab] = useState("loss");
  const [expanded, setExpanded] = useState(null);
  const [cheatData, setCheatData] = useState(null);
  const [explanations, setExplanations] = useState({});
  const [loadingExplain, setLoadingExplain] = useState(null);
  const containerRef = useRef(null);

  useEffect(() => {
    apiFetch("/api/cheatsheet/data").then(data => setCheatData(data)).catch(() => setCheatData({}));
    apiFetch("/api/cheatsheet/explanations").then(data => setExplanations(data)).catch(() => {});
  }, []);

  useEffect(() => {
    if (containerRef.current && window.MathJax) {
      MathJax.typesetPromise([containerRef.current]).catch(() => {});
    }
  }, [tab, expanded, explanations, cheatData]);

  const handleExplain = async (row, forceRefresh) => {
    setLoadingExplain(row.name);
    try {
      const data = await apiFetch("/api/cheatsheet/explain", {
        method: "POST",
        body: JSON.stringify({
          name: row.name, tag: row.tag || "general",
          equation: row.eq, symbols: row.symbols, used: row.used,
          force_refresh: forceRefresh,
        }),
      });
      setExplanations(prev => ({ ...prev, [row.name]: data.explanation }));
    } catch (e) {
      alert("Explanation failed: " + e.message);
    } finally {
      setLoadingExplain(null);
    }
  };

  const TABS = [
    { id: "loss",        label: "Loss Functions" },
    { id: "metrics",     label: "Eval Metrics" },
    { id: "activations", label: "Activations" },
    { id: "gradients",   label: "Gradients & Backprop" },
    { id: "linalg",      label: "Linear Algebra" },
  ];

  if (!cheatData) return <div className="flex items-center justify-center min-h-screen text-gray-500">Loading cheat sheet...</div>;

  const rows = cheatData[tab] || [];
  const counts = Object.fromEntries(Object.entries(cheatData).map(([k,v]) => [k, v.length]));

  return (
    <div className="max-w-5xl mx-auto p-4 pb-16 fade-in" ref={containerRef}>
      <div className="flex items-center gap-4 mb-6">
        <Btn onClick={onBack} variant="secondary">← Back</Btn>
        <div>
          <h1 className="text-2xl font-bold text-purple-700">Equation Cheat Sheet</h1>
          <p className="text-sm text-gray-500">{rows.length} equations · click row to expand · "Explain in Detail" uses RAG from your books</p>
        </div>
      </div>

      <div className="flex flex-wrap gap-2 mb-6">
        {TABS.map(t => (
          <button key={t.id} onClick={() => { setTab(t.id); setExpanded(null); }}
            className={`px-3 py-1 rounded-full text-sm font-semibold transition-colors ${
              tab === t.id ? "bg-purple-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}>
            {t.label} <span className="opacity-60">({counts[t.id]})</span>
          </button>
        ))}
      </div>

      <div className="grid grid-cols-12 gap-2 px-3 py-1 text-xs font-bold text-gray-400 uppercase tracking-wide border-b border-gray-200 mb-1">
        <div className="col-span-1"></div>
        <div className="col-span-3">Name</div>
        <div className="col-span-5">Equation</div>
        <div className="col-span-3">Used When</div>
      </div>

      <div className="space-y-1">
        {rows.map((row, i) => {
          const hasExplanation = !!explanations[row.name];
          const isLoading = loadingExplain === row.name;
          return (
            <div key={i} className="border border-gray-200 rounded-lg bg-white overflow-hidden shadow-sm">
              <div className="grid grid-cols-12 gap-2 p-3 cursor-pointer hover:bg-purple-50 transition-colors items-start"
                onClick={() => setExpanded(expanded === i ? null : i)}>
                <div className="col-span-1 text-purple-400 text-xs pt-1">{expanded === i ? "▼" : "▶"}</div>
                <div className="col-span-3 font-semibold text-gray-800 text-sm leading-snug">
                  {row.name}
                  {hasExplanation && <span className="ml-1 text-green-500 text-xs">●</span>}
                </div>
                <div className="col-span-5 text-sm" dangerouslySetInnerHTML={{__html: "$" + row.eq + "$"}} />
                <div className="col-span-3 text-xs text-gray-500 italic leading-snug">{row.used}</div>
              </div>

              {expanded === i && (
                <div className="bg-purple-50 border-t border-purple-100 p-4 space-y-3 text-sm">
                  <div>
                    <span className="text-xs font-bold text-purple-700 uppercase tracking-wide">Symbols: </span>
                    <span className="text-gray-700" dangerouslySetInnerHTML={{__html: row.symbols}} />
                  </div>
                  {row.note && (
                    <div>
                      <span className="text-xs font-bold text-purple-700 uppercase tracking-wide block mb-1">Notes:</span>
                      <span className="text-gray-700" dangerouslySetInnerHTML={{__html: row.note}} />
                    </div>
                  )}
                  {row.example && (
                    <div className="bg-white border border-purple-200 rounded p-3">
                      <span className="text-xs font-bold text-purple-700 uppercase tracking-wide block mb-2">Worked Example:</span>
                      <span className="text-gray-700" dangerouslySetInnerHTML={{__html: row.example}} />
                    </div>
                  )}
                  {hasExplanation && (
                    <div className="bg-green-50 border border-green-200 rounded p-3">
                      <span className="text-xs font-bold text-green-700 uppercase tracking-wide block mb-2">Detailed Explanation (saved):</span>
                      <Markdown content={explanations[row.name]} />
                    </div>
                  )}
                  <div className="flex gap-2 flex-wrap pt-1">
                    <Btn variant="secondary" className="text-xs py-1 px-3" disabled={isLoading}
                      onClick={(e) => { e.stopPropagation(); handleExplain(row, hasExplanation); }}>
                      {isLoading ? "Loading..." : hasExplanation ? "Refresh Explanation" : "Explain in Detail"}
                    </Btn>
                    {row.tag && (
                      <Btn variant="secondary" className="text-xs py-1 px-3"
                        onClick={(e) => { e.stopPropagation(); onDrillTag(row.tag); }}>
                        Drill: {row.tag} →
                      </Btn>
                    )}
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
