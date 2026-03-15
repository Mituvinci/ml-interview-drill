// FrameworkLearnScreen
const { useState, useEffect } = React;

const FW_COLORS = {
  green:  { tab: "bg-green-600 text-white",  badge: "bg-green-100 text-green-800",  border: "border-green-200",  header: "text-green-700" },
  orange: { tab: "bg-orange-500 text-white", badge: "bg-orange-100 text-orange-800", border: "border-orange-200", header: "text-orange-700" },
  blue:   { tab: "bg-blue-600 text-white",   badge: "bg-blue-100 text-blue-800",    border: "border-blue-200",   header: "text-blue-700" },
};
const FW_INACTIVE = "bg-gray-100 text-gray-600 hover:bg-gray-200";

function FrameworkLearnScreen({ onBack }) {
  const [catalog, setCatalog] = useState(null);
  const [activeFw, setActiveFw] = useState(null);
  const [activeProject, setActiveProject] = useState(null);
  const [activeFile, setActiveFile] = useState(null);
  const [fileContent, setFileContent] = useState(null);
  const [explanation, setExplanation] = useState(null);
  const [explLoading, setExplLoading] = useState(false);
  const [explError, setExplError] = useState(null);
  const [fileLoading, setFileLoading] = useState(false);

  useEffect(() => {
    apiFetch("/api/codelearn/catalog").then(data => {
      setCatalog(data);
      setActiveFw(Object.keys(data)[0]);
    }).catch(() => setCatalog({}));
  }, []);

  const loadFile = (fw, proj, filename) => {
    setActiveFile(filename);
    setFileContent(null);
    setExplanation(null);
    setExplError(null);
    setFileLoading(true);
    apiFetch(`/api/codelearn/file?framework=${fw}&project=${proj}&file=${encodeURIComponent(filename)}`)
      .then(d => setFileContent(d))
      .finally(() => setFileLoading(false));
  };

  const explain = (forceRefresh = false) => {
    if (!activeFile || !activeProject || !activeFw) return;
    setExplLoading(true);
    setExplError(null);
    apiFetch("/api/codelearn/explain", {
      method: "POST",
      body: JSON.stringify({ framework: activeFw, project: activeProject, file: activeFile, force_refresh: forceRefresh }),
    }).then(d => setExplanation(d.explanation))
      .catch(e => setExplError(e.message))
      .finally(() => setExplLoading(false));
  };

  if (!catalog) return <div className="flex items-center justify-center min-h-screen text-gray-400">Loading catalog...</div>;

  const fwKeys = Object.keys(catalog);
  const fw = catalog[activeFw];
  const proj = fw?.projects?.find(p => p.id === activeProject);
  const col = FW_COLORS[fw?.color] || FW_COLORS.blue;

  const resetFw = (key) => {
    setActiveFw(key); setActiveProject(null); setActiveFile(null); setFileContent(null); setExplanation(null);
  };
  const resetProject = () => {
    setActiveProject(null); setActiveFile(null); setFileContent(null); setExplanation(null);
  };

  return (
    <div className="max-w-5xl mx-auto p-4 pb-20 fade-in">
      <div className="flex items-center gap-4 mb-5">
        <Btn onClick={onBack} variant="secondary">← Back</Btn>
        <div>
          <h1 className="text-2xl font-bold text-teal-700">Framework Studio</h1>
          <p className="text-gray-500 text-sm">Learn by reading real production code · Claude explains everything</p>
        </div>
      </div>

      <div className="flex gap-2 mb-5 flex-wrap">
        {fwKeys.map(key => {
          const c = FW_COLORS[catalog[key].color] || FW_COLORS.blue;
          return (
            <button key={key} onClick={() => resetFw(key)}
              className={`px-4 py-2 rounded-lg font-semibold text-sm transition-colors ${activeFw === key ? c.tab : FW_INACTIVE}`}>
              {catalog[key].label}
            </button>
          );
        })}
      </div>

      {fw && (
        <div className="mb-5 bg-gray-50 border border-gray-200 rounded-xl p-4">
          <div className="text-xs text-gray-500 uppercase tracking-wide mb-1">{fw.tagline}</div>
          <div className="font-mono text-sm text-gray-700 mb-1"><span className="font-bold">Key concept:</span> {fw.key_concept}</div>
          <div className="text-sm text-gray-600">{fw.why_learn}</div>
        </div>
      )}

      {fw && !activeProject && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {fw.projects.map(p => (
            <button key={p.id}
              onClick={() => { setActiveProject(p.id); setActiveFile(null); setFileContent(null); setExplanation(null); }}
              className={`text-left border ${col.border} rounded-xl p-4 hover:shadow-md transition-shadow bg-white`}>
              <div className={`font-bold text-base mb-1 ${col.header}`}>{p.label}</div>
              <div className="text-gray-600 text-sm mb-2">{p.description}</div>
              <div className="font-mono text-xs text-gray-400 mb-2 leading-relaxed">{p.flow}</div>
              <div className="flex flex-wrap gap-1">
                {p.key_patterns?.slice(0, 2).map((kp, i) => (
                  <span key={i} className={`text-xs px-2 py-0.5 rounded-full ${col.badge}`}>{kp.split(' — ')[0]}</span>
                ))}
              </div>
            </button>
          ))}
        </div>
      )}

      {proj && (
        <div>
          <div className="flex items-center gap-3 mb-4">
            <button onClick={resetProject} className="text-gray-500 hover:text-gray-700 text-sm">← Projects</button>
            <h2 className={`font-bold text-xl ${col.header}`}>{proj.label}</h2>
          </div>

          <div className="bg-gray-50 border border-gray-200 rounded-xl p-4 mb-4">
            <div className="text-xs font-bold text-gray-500 uppercase mb-2">Key Patterns in This Project</div>
            <ul className="space-y-1">
              {proj.key_patterns?.map((kp, i) => (
                <li key={i} className="text-sm text-gray-700 flex gap-2">
                  <span className="text-teal-500 mt-0.5">▸</span>
                  <span>
                    <span className="font-mono font-bold text-gray-800">{kp.split(' — ')[0]}</span>
                    {kp.includes(' — ') ? ' — ' + kp.split(' — ')[1] : ''}
                  </span>
                </li>
              ))}
            </ul>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="md:col-span-1">
              <div className="text-xs font-bold text-gray-500 uppercase mb-2">Files (read order)</div>
              <div className="space-y-1">
                {[...proj.files].sort((a, b) => a.order - b.order).map(f => (
                  <button key={f.name} onClick={() => loadFile(activeFw, activeProject, f.name)}
                    className={`w-full text-left px-3 py-2 rounded-lg text-sm transition-colors ${
                      activeFile === f.name ? col.tab : "bg-gray-50 hover:bg-gray-100 text-gray-700"
                    }`}>
                    <div className="font-mono font-bold">{f.name}</div>
                    <div className={`text-xs mt-0.5 ${activeFile === f.name ? "text-white/80" : "text-gray-400"}`}>{f.role}</div>
                  </button>
                ))}
              </div>
            </div>

            <div className="md:col-span-2">
              {fileLoading && <div className="text-gray-400 p-4">Loading file...</div>}
              {fileContent && (
                <div>
                  <div className="flex gap-2 mb-3">
                    <button onClick={() => explain(false)} disabled={explLoading}
                      className="px-3 py-1.5 bg-teal-600 hover:bg-teal-700 text-white text-sm rounded-lg font-semibold disabled:opacity-50">
                      {explLoading ? "Explaining..." : explanation ? "Re-explain" : "Explain This File ▶"}
                    </button>
                    {explanation && (
                      <button onClick={() => explain(true)} disabled={explLoading}
                        className="px-3 py-1.5 bg-gray-100 hover:bg-gray-200 text-gray-600 text-sm rounded-lg disabled:opacity-50">
                        Refresh
                      </button>
                    )}
                  </div>

                  {!explanation && (
                    <pre className="bg-gray-900 text-green-300 text-xs p-4 rounded-xl overflow-auto max-h-96 leading-relaxed">
                      {fileContent.content}
                    </pre>
                  )}

                  {explError && <div className="text-red-500 text-sm p-3 bg-red-50 rounded-lg">{explError}</div>}

                  {explanation && (
                    <div className="space-y-3">
                      <div className="prose prose-sm max-w-none bg-white border border-gray-200 rounded-xl p-4 text-sm text-gray-800 leading-relaxed"
                        dangerouslySetInnerHTML={{ __html: explanation
                          .replace(/^## (.+)$/gm, '<h3 class="font-bold text-teal-700 text-base mt-4 mb-1">$1</h3>')
                          .replace(/^### (.+)$/gm, '<h4 class="font-bold text-gray-700 mt-3 mb-1">$1</h4>')
                          .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
                          .replace(/`([^`]+)`/g, '<code class="bg-gray-100 px-1 rounded text-xs font-mono text-rose-700">$1</code>')
                          .replace(/^[-*] (.+)$/gm, '<li class="ml-4 list-disc">$1</li>')
                          .replace(/\n\n/g, '<br/><br/>')
                        }}
                      />
                      <button onClick={() => setExplanation(null)}
                        className="text-xs text-gray-400 hover:text-gray-600">← Show code instead</button>
                    </div>
                  )}
                </div>
              )}
              {!fileContent && !fileLoading && (
                <div className="text-gray-400 text-sm p-8 text-center border-2 border-dashed border-gray-200 rounded-xl">
                  Select a file on the left to view its code and get a Claude explanation
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
