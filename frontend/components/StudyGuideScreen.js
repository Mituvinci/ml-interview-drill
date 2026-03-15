// StudyGuideScreen
const { useState, useEffect } = React;

const PHASE_COLORS = {
  blue:   { border: "border-blue-200",   header: "text-blue-700",   badge: "bg-blue-100 text-blue-700",   bar: "bg-blue-500" },
  green:  { border: "border-green-200",  header: "text-green-700",  badge: "bg-green-100 text-green-700",  bar: "bg-green-500" },
  orange: { border: "border-orange-200", header: "text-orange-700", badge: "bg-orange-100 text-orange-700", bar: "bg-orange-500" },
  yellow: { border: "border-yellow-200", header: "text-yellow-700", badge: "bg-yellow-100 text-yellow-700", bar: "bg-yellow-400" },
  teal:   { border: "border-teal-200",   header: "text-teal-700",   badge: "bg-teal-100 text-teal-700",   bar: "bg-teal-500" },
  purple: { border: "border-purple-200", header: "text-purple-700", badge: "bg-purple-100 text-purple-700", bar: "bg-purple-500" },
  red:    { border: "border-red-200",    header: "text-red-700",    badge: "bg-red-100 text-red-700",    bar: "bg-red-500" },
  indigo: { border: "border-indigo-200", header: "text-indigo-700", badge: "bg-indigo-100 text-indigo-700", bar: "bg-indigo-500" },
};

const PRIORITY_STYLE = {
  "CRITICAL":   "bg-red-100 text-red-700 font-bold",
  "HIGH":       "bg-orange-100 text-orange-700 font-bold",
  "MEDIUM":     "bg-yellow-100 text-yellow-700",
  "PRACTICAL":  "bg-teal-100 text-teal-700",
};

function StudyGuideScreen({ onBack, onDrillTag, onDrillQuestion }) {
  const [guide, setGuide] = useState(null);
  const [expanded, setExpanded] = useState(null);
  const [activeFilter, setActiveFilter] = useState("all");

  useEffect(() => {
    apiFetch("/api/study-guide").then(setGuide).catch(() => setGuide(null));
  }, []);

  if (!guide) return <div className="flex items-center justify-center min-h-screen text-gray-400">Loading guide...</div>;

  const totalDays = guide.quick_reference.total_estimated_days;
  const filteredPhases = activeFilter === "all"
    ? guide.phases
    : guide.phases.filter(p => p.priority === activeFilter);

  return (
    <div className="max-w-4xl mx-auto p-4 pb-20 fade-in">
      {/* Header */}
      <div className="flex items-center gap-4 mb-6">
        <Btn onClick={onBack} variant="secondary">← Back</Btn>
        <div>
          <h1 className="text-2xl font-bold text-indigo-700">{guide.title}</h1>
          <p className="text-gray-500 text-sm">{guide.subtitle}</p>
        </div>
      </div>

      {/* Amazon interview failures — top priority */}
      {guide.amazon_failures && guide.amazon_failures.length > 0 && (
        <div className="bg-red-50 border-2 border-red-400 rounded-xl p-4 mb-5">
          <div className="flex items-center gap-2 mb-3">
            <span className="text-red-600 text-lg font-bold">⚠</span>
            <span className="text-red-700 font-bold text-base">Amazon Interview — Questions You Couldn't Answer</span>
            <span className="text-xs text-red-400 ml-auto">Priority #1</span>
          </div>
          <div className="space-y-3">
            {guide.amazon_failures.map((f, i) => (
              <div key={i} className="bg-white border border-red-200 rounded-lg p-3">
                <p className="font-semibold text-gray-800 text-sm mb-1">"{f.question}"</p>
                <p className="text-xs text-gray-500 italic mb-2">{f.what_happened}</p>
                <div className="flex items-center gap-2 flex-wrap">
                  <button onClick={() => f.question_id ? onDrillQuestion(f.question_id) : onDrillTag(f.drill_tag)}
                    className="text-xs px-2 py-1 bg-red-100 text-red-700 rounded-lg hover:bg-red-200 font-semibold">
                    Drill this now →
                  </button>
                  {f.notes_file && (
                    <a href={`/notes/${f.notes_file}`} target="_blank" rel="noopener noreferrer"
                      className="text-xs px-2 py-1 bg-blue-50 text-blue-600 rounded-lg hover:bg-blue-100 border border-blue-200">
                      Open study notes ↗
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Note banner */}
      <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-4 mb-6 text-sm text-indigo-800">
        {guide.note}
      </div>

      {/* Quick reference cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-3 mb-6">
        {[
          { label: "1 week", text: guide.quick_reference.if_you_have_1_week, color: "border-red-200 bg-red-50" },
          { label: "2 weeks", text: guide.quick_reference.if_you_have_2_weeks, color: "border-orange-200 bg-orange-50" },
          { label: "1 month", text: guide.quick_reference.if_you_have_1_month, color: "border-green-200 bg-green-50" },
        ].map(c => (
          <div key={c.label} className={`border rounded-xl p-3 ${c.color}`}>
            <div className="font-bold text-sm mb-1">If you have {c.label}</div>
            <p className="text-xs text-gray-700 leading-relaxed">{c.text}</p>
          </div>
        ))}
      </div>

      {/* Daily routine */}
      <div className="bg-gray-50 border border-gray-200 rounded-xl p-3 mb-6 text-sm text-gray-700">
        <span className="font-bold">Daily routine: </span>{guide.quick_reference.daily_routine}
      </div>

      {/* Filter tabs */}
      <div className="flex gap-2 flex-wrap mb-4">
        {["all", "CRITICAL", "HIGH", "MEDIUM", "PRACTICAL"].map(f => (
          <button key={f} onClick={() => setActiveFilter(f)}
            className={`px-3 py-1 rounded-full text-xs font-semibold transition-colors ${
              activeFilter === f ? "bg-indigo-600 text-white" : "bg-gray-100 text-gray-600 hover:bg-gray-200"
            }`}>
            {f === "all" ? `All phases (${guide.phases.length})` : f}
          </button>
        ))}
      </div>

      {/* Phase list */}
      <div className="space-y-3">
        {filteredPhases.map((phase, i) => {
          const col = PHASE_COLORS[phase.color] || PHASE_COLORS.indigo;
          const isOpen = expanded === phase.phase;
          const pct = Math.round((phase.estimated_days / totalDays) * 100);

          return (
            <div key={phase.phase} className={`border ${col.border} rounded-xl bg-white overflow-hidden shadow-sm`}>
              {/* Phase header row */}
              <div className="p-4 cursor-pointer hover:bg-gray-50 transition-colors"
                onClick={() => setExpanded(isOpen ? null : phase.phase)}>
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold text-white ${col.bar}`}>
                    {phase.phase}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 flex-wrap">
                      <span className={`font-bold text-base ${col.header}`}>{phase.label}</span>
                      <span className={`text-xs px-2 py-0.5 rounded ${PRIORITY_STYLE[phase.priority] || ""}`}>
                        {phase.priority}
                      </span>
                      <span className="text-xs text-gray-400 ml-auto">{phase.estimated_days}d</span>
                    </div>
                    <p className="text-xs text-gray-500 mt-0.5 leading-snug">{phase.why}</p>
                  </div>
                  <span className="text-gray-400 text-xs ml-2">{isOpen ? "▼" : "▶"}</span>
                </div>
                {/* Progress bar representing time weight */}
                <div className="mt-2 w-full bg-gray-100 rounded h-1">
                  <div className={`h-1 rounded ${col.bar}`} style={{ width: `${pct}%` }} />
                </div>
              </div>

              {/* Expanded detail */}
              {isOpen && (
                <div className="border-t border-gray-100 p-4 space-y-4 bg-gray-50 text-sm">
                  {/* Topics to drill */}
                  <div>
                    <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Topics to drill</div>
                    <ul className="space-y-1">
                      {phase.drill_topics.map((t, j) => (
                        <li key={j} className="flex gap-2 text-gray-700">
                          <span className={`mt-0.5 ${col.header}`}>▸</span>
                          <span>{t}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* Interview tip */}
                  <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                    <div className="text-xs font-bold text-yellow-700 uppercase tracking-wide mb-1">Interview tip</div>
                    <p className="text-gray-700 leading-relaxed">{phase.interview_tip}</p>
                  </div>

                  {/* Book chapters */}
                  {phase.book_chapters.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-1">Source chapters</div>
                      <div className="flex flex-wrap gap-1">
                        {phase.book_chapters.map((ch, j) => (
                          <span key={j} className={`text-xs px-2 py-0.5 rounded-full ${col.badge}`}>{ch}</span>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Drill buttons for tagged topics */}
                  {phase.tags.length > 0 && (
                    <div>
                      <div className="text-xs font-bold text-gray-500 uppercase tracking-wide mb-2">Jump to drill</div>
                      <div className="flex flex-wrap gap-1">
                        {phase.tags.map(tag => (
                          <button key={tag} onClick={() => onDrillTag(tag)}
                            className={`text-xs px-2 py-1 rounded-lg border ${col.border} ${col.header} hover:opacity-80 transition-opacity bg-white`}>
                            {tag.replace(/_/g, " ")} →
                          </button>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      <p className="text-xs text-gray-400 text-center mt-6">
        {totalDays} total estimated study days · Trust the weak spot system — it will surface what needs more work.
      </p>
    </div>
  );
}
