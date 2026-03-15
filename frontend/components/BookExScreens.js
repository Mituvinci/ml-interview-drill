// BookExScreen, ExerciseDrillScreen, ExerciseFeedbackScreen
const { useState, useEffect } = React;

function BookExScreen({ onBack, onDrill }) {
  const [books, setBooks] = useState(null);
  const [error, setError] = useState(null);
  const [expanded, setExpanded] = useState(null);

  useEffect(() => {
    apiFetch("/api/exercises/books").then(setBooks).catch(e => setError(e.message));
  }, []);

  if (error) return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <Btn onClick={onBack} variant="secondary">← Home</Btn>
      <div className="text-red-600 mt-6">{error}</div>
      <p className="text-gray-500 text-sm mt-3">
        Run <code className="bg-gray-100 px-1 rounded text-indigo-600">uv run python extract_exercises.py</code> first, then restart the server.
      </p>
    </div>
  );
  if (!books) return <div className="text-gray-500 text-center mt-20">Loading...</div>;

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Home</Btn>
        <h2 className="text-xl font-bold text-indigo-600">Book Exercises</h2>
      </div>
      <p className="text-gray-500 text-sm mb-6">
        Real end-of-chapter exercises extracted from the books. Pick a chapter to drill.
      </p>
      <div className="space-y-4">
        {books.map(book => (
          <Card key={book.key}>
            <button onClick={() => setExpanded(expanded === book.key ? null : book.key)}
              className="w-full flex items-center justify-between text-left">
              <span className="text-indigo-600 font-semibold">{book.label}</span>
              <span className="text-gray-500 text-sm">
                {book.chapters.length} chapters {expanded === book.key ? "▼" : "▶"}
              </span>
            </button>
            {expanded === book.key && (
              <div className="mt-4 space-y-1">
                {book.chapters.map(ch => (
                  <div key={ch.num} className="flex items-center justify-between py-2 border-b border-gray-200">
                    <span className="text-gray-700 text-sm flex-1">
                      <span className="text-gray-500 mr-2">Ch {ch.num}</span>{ch.title}
                    </span>
                    <div className="flex items-center gap-2 ml-3">
                      <span className="text-gray-400 text-xs">{ch.count}q</span>
                      <Btn onClick={() => onDrill(book, ch.num)} variant="secondary" className="text-xs py-1 px-3">Drill</Btn>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </Card>
        ))}
      </div>
    </div>
  );
}

function ExerciseDrillScreen({ book, chapterNum, startQIndex, onBack, onFeedback }) {
  const [chapter, setChapter] = useState(null);
  const [qIndex, setQIndex] = useState(startQIndex || 0);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [modelAnswer, setModelAnswer] = useState(null);
  const [bookPassages, setBookPassages] = useState([]);
  const [showModelAnswer, setShowModelAnswer] = useState(false);
  const [showPassages, setShowPassages] = useState(false);
  const [modelLoading, setModelLoading] = useState(false);

  const { listening, timeLeft, start: startSpeech, stop: stopSpeech, supported } = useSpeechToText((text) => setAnswer(text));

  useEffect(() => {
    apiFetch(`/api/exercises/${book.key}/${chapterNum}`).then(setChapter).catch(e => setError(e.message));
  }, [book.key, chapterNum]);

  useEffect(() => {
    setAnswer(""); setModelAnswer(null); setBookPassages([]); setShowModelAnswer(false); setShowPassages(false); setError(null);
  }, [qIndex]);

  const revealModelAnswer = async (forceRefresh = false) => {
    if (modelAnswer && !forceRefresh) { setShowModelAnswer(v => !v); return; }
    setModelLoading(true);
    try {
      const r = await apiFetch("/api/exercises/model-answer", {
        method: "POST",
        body: JSON.stringify({ book: book.key, chapter: chapterNum, q_index: qIndex, force_refresh: forceRefresh }),
      });
      setModelAnswer(r.model_answer);
      setBookPassages(r.book_passages || []);
      setShowModelAnswer(true);
      setShowPassages(false);
      if (window.MathJax) setTimeout(() => MathJax.typesetPromise(), 100);
    } catch (e) { setError(e.message); } finally { setModelLoading(false); }
  };

  const submit = async () => {
    if (!answer.trim()) return;
    setLoading(true); setError(null);
    try {
      const result = await apiFetch("/api/exercises/evaluate", {
        method: "POST",
        body: JSON.stringify({ book: book.key, chapter: chapterNum, q_index: qIndex, answer }),
      });
      const q = chapter.questions[qIndex];
      onFeedback({ question: { question_text: q.text, question_id: q.id }, answer, result, book, chapterNum, qIndex, total: chapter.count });
    } catch (e) { setError(e.message); } finally { setLoading(false); }
  };

  if (error && !chapter) return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <Btn onClick={onBack} variant="secondary">← Books</Btn>
      <div className="text-red-600 mt-6">{error}</div>
    </div>
  );
  if (!chapter) return <div className="text-gray-500 text-center mt-20">Loading...</div>;

  const q = chapter.questions[qIndex];
  const total = chapter.count;

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-4">
        <Btn onClick={onBack} variant="secondary">← Books</Btn>
        <h2 className="text-xl font-bold text-indigo-600">{book.label}</h2>
        <Badge label={`Ch ${chapterNum}`} color="blue" />
      </div>
      <div className="mb-4">
        <div className="flex justify-between text-xs text-gray-500 mb-1">
          <span>Exercise {qIndex + 1} of {total}</span>
          <span>{chapter.title}</span>
        </div>
        <div className="w-full bg-gray-100 rounded h-1">
          <div className="bg-indigo-600 h-1 rounded transition-all" style={{ width: `${((qIndex + 1) / total) * 100}%` }} />
        </div>
      </div>
      <Card>
        <p className="text-lg text-gray-900 mb-4 leading-relaxed">{q.text}</p>
        <div className="mb-4">
          <div className="flex items-center gap-3 flex-wrap">
            <button onClick={() => revealModelAnswer(false)} disabled={modelLoading}
              className="text-indigo-600 hover:text-indigo-500 text-sm flex items-center gap-1 disabled:opacity-50">
              {modelLoading ? "⏳ Generating..." : showModelAnswer ? "▼ Hide book answer" : "▶ Reveal book answer"}
            </button>
            {showModelAnswer && bookPassages.length === 0 && !modelLoading && (
              <button onClick={() => revealModelAnswer(true)} disabled={modelLoading}
                className="text-xs text-orange-500 hover:text-orange-700 border border-orange-200 rounded px-2 py-0.5 disabled:opacity-50">
                ↺ Refresh with book passages
              </button>
            )}
          </div>
          {showModelAnswer && modelAnswer && (
            <div className="mt-3 space-y-2">
              <div className="border border-indigo-200 rounded-lg p-4 text-gray-700 text-sm bg-indigo-50">
                <Markdown content={modelAnswer} />
              </div>
              {bookPassages.length > 0 && (
                <div>
                  <button onClick={() => setShowPassages(v => !v)}
                    className="text-xs text-indigo-500 hover:text-indigo-700 flex items-center gap-1">
                    {showPassages ? "▼" : "▶"} Book evidence ({bookPassages.length} passage{bookPassages.length > 1 ? "s" : ""} retrieved from {book.label})
                  </button>
                  {showPassages && (
                    <div className="mt-2 space-y-2">
                      {bookPassages.map((p, i) => (
                        <div key={i} className="border-l-4 border-indigo-300 pl-3 bg-white rounded-r p-2">
                          <div className="text-xs font-semibold text-indigo-600 mb-1">{p.source}</div>
                          <p className="text-xs text-gray-600 italic leading-relaxed">{p.text}</p>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
        <div className="relative">
          <textarea value={answer} onChange={e => setAnswer(e.target.value)}
            placeholder="Write your answer here — or use the mic."
            className="w-full h-44 bg-white border border-gray-300 rounded p-3 text-gray-900 text-sm focus:border-indigo-500 focus:outline-none"
            disabled={loading} />
          {supported && (
            <button onClick={listening ? stopSpeech : startSpeech} disabled={loading}
              title={listening ? "Stop recording" : "Speak your answer"}
              className={`absolute bottom-3 right-3 w-9 h-9 rounded-full flex items-center justify-center transition-colors focus:outline-none
                ${listening ? "bg-red-600 hover:bg-red-500 animate-pulse" : "bg-gray-400 hover:bg-gray-500"}`}>
              {listening ? "■" : "🎤"}
            </button>
          )}
        </div>
        {listening && (
          <p className="text-xs text-red-600 mt-1 animate-pulse flex items-center gap-2">
            Recording... click to stop.
            <span className="text-xs text-gray-500 ml-2">{Math.floor(timeLeft/60)}:{String(timeLeft%60).padStart(2,'0')}</span>
          </p>
        )}
        {error && <div className="text-red-600 text-sm mt-2">{error}</div>}
        <div className="flex gap-3 mt-4 flex-wrap">
          <Btn onClick={submit} disabled={loading || !answer.trim()}>{loading ? "Evaluating..." : "Submit Answer"}</Btn>
          <Btn onClick={() => setQIndex(i => Math.min(total - 1, i + 1))} variant="secondary" disabled={loading || qIndex >= total - 1}>Skip →</Btn>
          <div className="ml-auto flex gap-2">
            <Btn onClick={() => setQIndex(i => Math.max(0, i - 1))} variant="secondary" disabled={qIndex === 0} className="text-xs">← Prev</Btn>
            <Btn onClick={() => setQIndex(i => Math.min(total - 1, i + 1))} variant="secondary" disabled={qIndex >= total - 1} className="text-xs">Next →</Btn>
          </div>
        </div>
      </Card>
    </div>
  );
}

function ExerciseFeedbackScreen({ data, onNext, onBack, onForceRefresh }) {
  const { question, answer, result, total, qIndex } = data;
  const [showImproved, setShowImproved] = useState(false);
  useEffect(() => { if (window.MathJax) MathJax.typesetPromise(); }, [data, showImproved]);

  const score = result.score ?? 0;
  const scoreColor = score >= 7 ? "text-green-600" : score >= 4 ? "text-yellow-600" : "text-red-600";
  const verdictColor = { correct: "green", partial: "yellow", incorrect: "red" };
  const isLast = total !== undefined && qIndex >= total - 1;

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Books</Btn>
        <h2 className="text-xl font-bold text-indigo-600">Feedback</h2>
        <Badge label="Book Exercise" color="blue" />
      </div>
      <Card className="mb-4 text-center">
        <div className={`score-ring ${scoreColor}`}>{score}<span className="text-2xl text-gray-500">/10</span></div>
        <div className="mt-1 flex justify-center gap-2 flex-wrap">
          <Badge label={result.verdict} color={verdictColor[result.verdict] || "gray"} />
          {result.from_cache ? <Badge label="Loaded from notes" color="yellow" /> : <Badge label="Saved to journal" color="green" />}
        </div>
        <p className="text-gray-500 text-sm mt-2">{question.question_text}</p>
      </Card>
      {answer && (
        <Card className="mb-3 border-gray-200">
          <h3 className="text-gray-500 font-semibold mb-1">Your Answer</h3>
          <p className="text-gray-800 text-sm whitespace-pre-wrap">{answer}</p>
        </Card>
      )}
      {result.what_you_got_right && (
        <Card className="mb-3 border-green-300">
          <h3 className="text-green-600 font-semibold mb-1">What you got right</h3>
          <Markdown content={result.what_you_got_right} />
        </Card>
      )}
      {result.what_is_missing && (
        <Card className="mb-3 border-red-300">
          <h3 className="text-red-600 font-semibold mb-1">What is missing</h3>
          <Markdown content={result.what_is_missing} />
        </Card>
      )}
      {result.book_reference && (
        <Card className="mb-3 border-indigo-300">
          <h3 className="text-indigo-600 font-semibold mb-1">Book Reference</h3>
          <blockquote className="border-l-2 border-indigo-600 pl-3 text-gray-700 text-sm italic">{result.book_reference}</blockquote>
        </Card>
      )}
      {result.improved_answer && (
        <Card className="mb-3">
          <button onClick={() => setShowImproved(!showImproved)}
            className="text-gray-500 hover:text-gray-800 text-sm font-semibold w-full text-left">
            {showImproved ? "▼" : "▶"} Improved Answer
          </button>
          {showImproved && <div className="text-gray-800 text-sm mt-2"><Markdown content={result.improved_answer} /></div>}
        </Card>
      )}
      {result.follow_up_question && (
        <Card className="mb-5 border-yellow-300">
          <h3 className="text-yellow-600 font-semibold mb-1">Follow-up Challenge</h3>
          <p className="text-gray-800 text-sm">{result.follow_up_question}</p>
        </Card>
      )}
      <div className="flex gap-3 flex-wrap">
        {!isLast && <Btn onClick={onNext}>Next Exercise →</Btn>}
        {isLast && <Btn onClick={onBack} variant="secondary">← Back to Books</Btn>}
        {result.cache_key && (
          <Btn onClick={() => onForceRefresh(result.cache_key)} variant="secondary" className="text-xs text-gray-500">
            Force Re-evaluate
          </Btn>
        )}
      </div>
    </div>
  );
}
