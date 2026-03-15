// DrillScreen, FeedbackScreen, FollowUpScreen, useSpeechToText
const { useState, useEffect, useCallback, useRef } = React;

function useSpeechToText(onResult) {
  const [listening, setListening] = useState(false);
  const [timeLeft, setTimeLeft] = useState(300);
  const recognitionRef = useRef(null);
  const shouldListenRef = useRef(false);
  const endTimeRef = useRef(null);
  const timerRef = useRef(null);

  const startRecognition = useCallback(() => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) return;
    const rec = new SpeechRecognition();
    rec.continuous = true;
    rec.interimResults = false;
    rec.lang = 'en-US';
    rec.onresult = (e) => {
      const text = Array.from(e.results).map(r => r[0].transcript).join(' ');
      onResult(text);
    };
    rec.onend = () => {
      if (shouldListenRef.current && Date.now() < endTimeRef.current) {
        try { rec.start(); } catch(e) {}
      } else {
        shouldListenRef.current = false;
        setListening(false);
        clearInterval(timerRef.current);
      }
    };
    recognitionRef.current = rec;
    try { rec.start(); } catch(e) {}
  }, [onResult]);

  const start = useCallback(() => {
    shouldListenRef.current = true;
    endTimeRef.current = Date.now() + 300000;
    setTimeLeft(300);
    setListening(true);
    timerRef.current = setInterval(() => {
      const remaining = Math.max(0, Math.ceil((endTimeRef.current - Date.now()) / 1000));
      setTimeLeft(remaining);
      if (remaining <= 0) {
        shouldListenRef.current = false;
        recognitionRef.current?.stop();
        clearInterval(timerRef.current);
        setListening(false);
      }
    }, 1000);
    startRecognition();
  }, [startRecognition]);

  const stop = useCallback(() => {
    shouldListenRef.current = false;
    clearInterval(timerRef.current);
    recognitionRef.current?.stop();
    setListening(false);
  }, []);

  const supported = !!(window.SpeechRecognition || window.webkitSpeechRecognition);
  return { listening, timeLeft, start, stop, supported };
}

function DrillScreen({ onBack, onFeedback, filterTag = null, startQuestionId = null }) {
  const [question, setQuestion] = useState(null);
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isFirstQuestion, setIsFirstQuestion] = useState(true);

  const { listening, timeLeft, start: startSpeech, stop: stopSpeech, supported } = useSpeechToText((text) => setAnswer(text));

  const fetchQuestion = useCallback(async (forceId = null) => {
    setError(null);
    try {
      let url;
      if (forceId) {
        url = `/api/drill/${forceId}`;
      } else if (filterTag) {
        url = `/api/drill?tag=${encodeURIComponent(filterTag)}`;
      } else {
        url = "/api/drill";
      }
      const q = await apiFetch(url);
      setQuestion(q);
      setAnswer("");
    } catch (e) { setError(e.message); }
  }, [filterTag]);

  useEffect(() => {
    if (startQuestionId && isFirstQuestion) {
      fetchQuestion(startQuestionId);
      setIsFirstQuestion(false);
    } else {
      fetchQuestion();
    }
  }, []);

  const submit = async () => {
    if (!answer.trim()) return;
    setLoading(true);
    setError(null);
    try {
      const result = await apiFetch("/api/evaluate", {
        method: "POST",
        body: JSON.stringify({ question_id: question.question_id, answer }),
      });
      onFeedback({ question, answer, result });
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  const diffColor = { easy: "green", medium: "yellow", hard: "red" };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Home</Btn>
        <h2 className="text-xl font-bold text-indigo-600">Drill</h2>
        {filterTag && <Badge label={`Weak spot: ${filterTag}`} color="red" />}
      </div>

      {error && <div className="bg-red-50 border border-red-300 rounded p-3 mb-4 text-red-700">{error}</div>}

      {question ? (
        <Card>
          <div className="flex gap-2 mb-4 flex-wrap">
            <Badge label={question.tag} color="blue" />
            <Badge label={question.difficulty} color={diffColor[question.difficulty] || "gray"} />
            {question.source === "Generated" && <Badge label="AI Generated" color="green" />}
            <Badge label={`Q${question.question_id}`} />
          </div>
          <p className="text-lg text-gray-900 mb-5 leading-relaxed">{question.question_text}</p>
          {question.hint && <p className="text-sm text-indigo-600 bg-indigo-50 rounded p-2 mb-4">Hint: {question.hint}</p>}

          <div className="relative">
            <textarea
              value={answer}
              onChange={e => setAnswer(e.target.value)}
              placeholder="Write your answer here — or use the mic to speak it."
              className="w-full h-48 bg-white border border-gray-300 rounded p-3 text-gray-900 text-sm focus:border-indigo-500 focus:outline-none"
              disabled={loading}
            />
            {supported && (
              <button
                onClick={listening ? stopSpeech : startSpeech}
                disabled={loading}
                title={listening ? "Stop recording" : "Speak your answer"}
                className={`absolute bottom-3 right-3 w-9 h-9 rounded-full flex items-center justify-center transition-colors focus:outline-none
                  ${listening ? "bg-red-600 hover:bg-red-500 animate-pulse" : "bg-gray-400 hover:bg-gray-500"}`}
              >
                {listening ? "■" : "🎤"}
              </button>
            )}
          </div>

          {listening && (
            <p className="text-xs text-red-600 mt-1 animate-pulse flex items-center gap-2">
              Recording... click the button to stop.
              <span className="text-xs text-gray-500 ml-2">{Math.floor(timeLeft/60)}:{String(timeLeft%60).padStart(2,'0')}</span>
            </p>
          )}
          {!supported && (
            <p className="text-xs text-gray-500 mt-1">Speech input not supported in this browser. Use Chrome or Edge.</p>
          )}

          <div className="flex gap-3 mt-4">
            <Btn onClick={submit} disabled={loading || !answer.trim()}>
              {loading ? "Evaluating..." : "Submit Answer"}
            </Btn>
            <Btn onClick={fetchQuestion} variant="secondary" disabled={loading}>Skip</Btn>
          </div>
        </Card>
      ) : !error ? (
        <div className="text-gray-500 text-center mt-20">Loading question...</div>
      ) : null}
    </div>
  );
}

function FeedbackScreen({ data, onNext, onFollowUp, onBack, onForceRefresh }) {
  const { question, answer, result } = data;
  const [showImproved, setShowImproved] = useState(false);
  useEffect(() => { if (window.MathJax) MathJax.typesetPromise(); }, [data, showImproved]);
  const score = result.score ?? 0;
  const scoreColor = score >= 7 ? "text-green-600" : score >= 4 ? "text-yellow-600" : "text-red-600";
  const verdictColor = { correct: "green", partial: "yellow", incorrect: "red" };

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Home</Btn>
        <h2 className="text-xl font-bold text-indigo-600">Feedback</h2>
      </div>

      <Card className="mb-4 text-center">
        <div className={`score-ring ${scoreColor}`}>{score}<span className="text-2xl text-gray-500">/10</span></div>
        <div className="mt-1 flex justify-center gap-2 flex-wrap">
          <Badge label={result.verdict} color={verdictColor[result.verdict] || "gray"} />
          {result.from_cache
            ? <Badge label="Loaded from notes" color="yellow" />
            : <Badge label="Saved to journal" color="green" />}
        </div>
        <p className="text-gray-500 text-sm mt-2">{question.question_text}</p>
      </Card>

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
          <blockquote className="border-l-2 border-indigo-600 pl-3 text-gray-700 text-sm italic">
            {result.book_reference}
          </blockquote>
        </Card>
      )}
      {result.improved_answer && (
        <Card className="mb-3">
          <button onClick={() => setShowImproved(!showImproved)}
            className="text-gray-500 hover:text-gray-800 text-sm font-semibold w-full text-left">
            {showImproved ? "▼" : "▶"} Improved Answer
          </button>
          {showImproved && (
            <div className="text-gray-800 text-sm mt-2"><Markdown content={result.improved_answer} /></div>
          )}
        </Card>
      )}
      {result.follow_up_question && (
        <Card className="mb-5 border-yellow-300">
          <h3 className="text-yellow-600 font-semibold mb-1">Follow-up Challenge</h3>
          <p className="text-gray-800 text-sm">{result.follow_up_question}</p>
        </Card>
      )}

      <div className="flex gap-3 flex-wrap">
        {result.follow_up_question && (
          <Btn onClick={() => onFollowUp(result.follow_up_question)} variant="secondary">Answer Follow-up</Btn>
        )}
        <Btn onClick={onNext}>Next Question →</Btn>
        {result.cache_key && (
          <Btn onClick={() => onForceRefresh(result.cache_key)} variant="secondary" className="text-xs text-gray-500">
            Force Re-evaluate
          </Btn>
        )}
      </div>
    </div>
  );
}

function FollowUpScreen({ originalQuestion, followUpText, onBack, onDone }) {
  const [answer, setAnswer] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  const submit = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await apiFetch("/api/evaluate", {
        method: "POST",
        body: JSON.stringify({ question_id: originalQuestion.question_id, answer }),
      });
      setResult(res);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  };

  if (result) {
    return (
      <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
        <Card className="mb-4">
          <h3 className="text-indigo-600 font-semibold mb-2">Follow-up Evaluation</h3>
          <div className="text-2xl font-bold mb-2">
            <span className={result.score >= 7 ? "text-green-600" : result.score >= 4 ? "text-yellow-600" : "text-red-600"}>
              {result.score}/10
            </span>
          </div>
          <p className="text-gray-700 text-sm mb-2">{result.what_is_missing}</p>
          {result.improved_answer && <p className="text-gray-500 text-sm italic">{result.improved_answer}</p>}
        </Card>
        <Btn onClick={onDone}>Next Question →</Btn>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Back</Btn>
        <h2 className="text-xl font-bold text-yellow-600">Follow-up</h2>
      </div>
      <Card>
        <p className="text-gray-900 mb-4">{followUpText}</p>
        {error && <div className="text-red-600 text-sm mb-3">{error}</div>}
        <textarea
          value={answer}
          onChange={e => setAnswer(e.target.value)}
          placeholder="Your answer..."
          className="w-full h-36 bg-white border border-gray-300 rounded p-3 text-gray-900 text-sm focus:border-indigo-500 focus:outline-none"
          disabled={loading}
        />
        <div className="mt-3">
          <Btn onClick={submit} disabled={loading || !answer.trim()}>
            {loading ? "Evaluating..." : "Submit"}
          </Btn>
        </div>
      </Card>
    </div>
  );
}
