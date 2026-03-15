// JournalScreen, JournalEntryScreen
const { useState, useEffect } = React;

function JournalScreen({ onBack, onViewEntry }) {
  const [sessions, setSessions] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiFetch("/api/journal").then(setSessions).catch(e => setError(e.message));
  }, []);

  const verdictIcon = { correct: "✓", partial: "◑", incorrect: "✗" };
  const verdictColor = { correct: "text-green-600", partial: "text-yellow-600", incorrect: "text-red-600" };

  if (error) return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <Btn onClick={onBack} variant="secondary">← Home</Btn>
      <div className="text-red-600 mt-6">{error}</div>
    </div>
  );
  if (!sessions) return <div className="text-gray-500 text-center mt-20">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Home</Btn>
        <h2 className="text-xl font-bold text-indigo-600">Study Journal</h2>
      </div>
      {sessions.length === 0 ? (
        <Card><p className="text-gray-500 text-center">No sessions yet. Start drilling!</p></Card>
      ) : (
        <div className="space-y-4">
          {sessions.map(session => (
            <Card key={session.session_id}>
              <div className="flex justify-between items-center mb-3">
                <span className="text-indigo-600 font-semibold">
                  {new Date(session.date).toLocaleDateString("en-US", { year: "numeric", month: "long", day: "numeric" })}
                </span>
                <span className="text-xs text-gray-500">
                  {session.summary.questions_attempted} questions · avg {session.summary.avg_score}/10
                </span>
              </div>
              <div className="space-y-1">
                {session.entries.map((entry, i) => (
                  <button key={i}
                    onClick={() => entry.cache_key ? onViewEntry(entry.cache_key) : null}
                    className={`w-full flex items-center justify-between text-sm py-1.5 px-2 rounded transition-colors text-left
                      ${entry.cache_key ? "hover:bg-gray-50 cursor-pointer" : "cursor-default opacity-60"}`}
                    title={entry.cache_key ? "Click to view feedback" : "No saved feedback"}
                  >
                    <span className={`w-5 font-bold ${verdictColor[entry.verdict] || "text-gray-500"}`}>
                      {verdictIcon[entry.verdict] || "·"}
                    </span>
                    <span className="flex-1 text-gray-700 truncate mx-2">{entry.question_text}</span>
                    <span className={`text-xs font-semibold ${verdictColor[entry.verdict] || "text-gray-500"}`}>
                      {entry.score}/10
                    </span>
                    {!entry.cache_key && <span className="text-xs text-gray-400 ml-2">no saved feedback</span>}
                  </button>
                ))}
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}

function JournalEntryScreen({ cacheKey, onBack }) {
  const [entry, setEntry] = useState(null);
  const [error, setError] = useState(null);
  const [showImproved, setShowImproved] = useState(false);

  useEffect(() => {
    if (!cacheKey) { setError("No saved feedback for this entry."); return; }
    apiFetch(`/api/journal/${cacheKey}`).then(setEntry).catch(e => setError(e.message));
  }, [cacheKey]);

  useEffect(() => { if (entry && window.MathJax) MathJax.typesetPromise(); }, [entry, showImproved]);

  if (error) return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <Btn onClick={onBack} variant="secondary">← Journal</Btn>
      <div className="text-red-600 mt-6">{error}</div>
    </div>
  );
  if (!entry) return <div className="text-gray-500 text-center mt-20">Loading...</div>;

  const r = entry.evaluation;
  const score = r.score ?? 0;
  const scoreColor = score >= 7 ? "text-green-600" : score >= 4 ? "text-yellow-600" : "text-red-600";
  const verdictColor = { correct: "green", partial: "yellow", incorrect: "red" };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Journal</Btn>
        <h2 className="text-xl font-bold text-indigo-600">Past Feedback</h2>
        <Badge label="Loaded from notes" color="yellow" />
      </div>
      <Card className="mb-4 text-center">
        <div className={`score-ring ${scoreColor}`}>{score}<span className="text-2xl text-gray-500">/10</span></div>
        <div className="mt-1"><Badge label={r.verdict} color={verdictColor[r.verdict] || "gray"} /></div>
        <p className="text-gray-500 text-sm mt-2">{entry.question_text}</p>
      </Card>
      {entry.user_answer && (
        <Card className="mb-3 border-gray-300">
          <h3 className="text-gray-500 font-semibold mb-1">Your Answer</h3>
          <p className="text-gray-800 text-sm whitespace-pre-wrap">{entry.user_answer}</p>
        </Card>
      )}
      {r.what_you_got_right && (
        <Card className="mb-3 border-green-300">
          <h3 className="text-green-600 font-semibold mb-1">What you got right</h3>
          <Markdown content={r.what_you_got_right} />
        </Card>
      )}
      {r.what_is_missing && (
        <Card className="mb-3 border-red-300">
          <h3 className="text-red-600 font-semibold mb-1">What is missing</h3>
          <Markdown content={r.what_is_missing} />
        </Card>
      )}
      {r.book_reference && (
        <Card className="mb-3 border-indigo-300">
          <h3 className="text-indigo-600 font-semibold mb-1">Book Reference</h3>
          <blockquote className="border-l-2 border-indigo-600 pl-3 text-gray-700 text-sm italic">{r.book_reference}</blockquote>
        </Card>
      )}
      {r.improved_answer && (
        <Card className="mb-3">
          <button onClick={() => setShowImproved(!showImproved)}
            className="text-gray-500 hover:text-gray-800 text-sm font-semibold w-full text-left">
            {showImproved ? "▼" : "▶"} Improved Answer
          </button>
          {showImproved && <div className="text-gray-800 text-sm mt-2"><Markdown content={r.improved_answer} /></div>}
        </Card>
      )}
      {r.follow_up_question && (
        <Card className="mb-4 border-yellow-300">
          <h3 className="text-yellow-600 font-semibold mb-1">Follow-up Challenge</h3>
          <p className="text-gray-800 text-sm">{r.follow_up_question}</p>
        </Card>
      )}
      <p className="text-xs text-gray-400 mt-2">
        Reviewed {entry.times_reviewed}x · Cached {new Date(entry.cached_at).toLocaleDateString()}
      </p>
    </div>
  );
}
