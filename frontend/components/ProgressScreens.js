// ProgressScreen, WeakSpotsScreen
const { useState, useEffect } = React;

function ProgressScreen({ onBack }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiFetch("/api/progress").then(setData).catch(e => setError(e.message));
  }, []);

  if (error) return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <Btn onClick={onBack} variant="secondary">← Home</Btn>
      <div className="text-red-600 mt-6">{error}</div>
    </div>
  );
  if (!data) return <div className="text-gray-500 text-center mt-20">Loading...</div>;

  const topics = Object.entries(data.all_topics || {}).sort((a, b) => a[1].score_avg - b[1].score_avg);

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Home</Btn>
        <h2 className="text-xl font-bold text-indigo-600">Progress</h2>
      </div>

      <div className="grid grid-cols-3 gap-3 mb-6">
        <Card className="text-center">
          <div className="text-2xl font-bold text-indigo-600">{data.total_attempts}</div>
          <div className="text-gray-500 text-xs mt-1">Total Attempts</div>
        </Card>
        <Card className="text-center">
          <div className="text-2xl font-bold text-green-600">{data.streak_days}</div>
          <div className="text-gray-500 text-xs mt-1">Day Streak</div>
        </Card>
        <Card className="text-center">
          <div className="text-2xl font-bold text-red-600">{Object.keys(data.weak_spots || {}).length}</div>
          <div className="text-gray-500 text-xs mt-1">Weak Spots</div>
        </Card>
      </div>

      {topics.length > 0 ? (
        <Card className="mb-4">
          <h3 className="text-gray-700 font-semibold mb-4">Topic Scores</h3>
          <div className="space-y-3">
            {topics.map(([tag, stats]) => {
              const avg = stats.score_avg ?? 0;
              const pct = (avg / 10) * 100;
              const barColor = avg >= 7 ? "bg-green-600" : avg >= 4 ? "bg-yellow-600" : "bg-red-600";
              return (
                <div key={tag}>
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-gray-700">{tag}</span>
                    <span className="text-gray-500">{avg.toFixed(1)}/10 · {stats.attempts} attempts</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded h-2">
                    <div className={`${barColor} h-2 rounded transition-all`} style={{ width: `${pct}%` }} />
                  </div>
                </div>
              );
            })}
          </div>
        </Card>
      ) : (
        <Card><p className="text-gray-500 text-center">No attempts yet. Start drilling!</p></Card>
      )}

      {data.recent_sessions?.length > 0 && (
        <Card>
          <h3 className="text-gray-700 font-semibold mb-3">Recent Sessions</h3>
          <div className="space-y-1">
            {[...data.recent_sessions].reverse().map((s, i) => (
              <div key={i} className="flex justify-between text-xs text-gray-500">
                <span>{s.tag}</span>
                <span className={s.score >= 7 ? "text-green-600" : s.score >= 4 ? "text-yellow-600" : "text-red-600"}>
                  {s.score}/10
                </span>
                <span>{new Date(s.timestamp).toLocaleDateString()}</span>
              </div>
            ))}
          </div>
        </Card>
      )}
    </div>
  );
}

function WeakSpotsScreen({ onBack, onDrill, onDrillTag }) {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    apiFetch("/api/progress").then(setData).catch(e => setError(e.message));
  }, []);

  if (error) return (
    <div className="max-w-3xl mx-auto py-10 px-4">
      <Btn onClick={onBack} variant="secondary">← Home</Btn>
      <div className="text-red-600 mt-6">{error}</div>
    </div>
  );
  if (!data) return <div className="text-gray-500 text-center mt-20">Loading...</div>;

  const weak = Object.entries(data.weak_spots || {}).sort((a, b) => a[1].score_avg - b[1].score_avg);

  return (
    <div className="max-w-3xl mx-auto py-10 px-4 fade-in">
      <div className="flex items-center gap-3 mb-6">
        <Btn onClick={onBack} variant="secondary">← Home</Btn>
        <h2 className="text-xl font-bold text-red-600">Weak Spots</h2>
      </div>
      {weak.length === 0 ? (
        <Card><p className="text-gray-500 text-center">No weak spots yet — keep drilling to find them.</p></Card>
      ) : (
        <div className="space-y-3">
          {weak.map(([tag, stats]) => (
            <Card key={tag} className="border-red-300 flex items-center justify-between">
              <div>
                <div className="text-red-600 font-semibold">{tag}</div>
                <div className="text-xs text-gray-500 mt-1">
                  avg {stats.score_avg.toFixed(1)}/10 · {stats.attempts} attempts · {stats.correct} correct
                </div>
              </div>
              <Btn onClick={() => onDrillTag(tag)} variant="danger">Drill This</Btn>
            </Card>
          ))}
        </div>
      )}
    </div>
  );
}
