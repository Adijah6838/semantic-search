import { useState } from "react";
const API = "http://127.0.0.1:8002/api";
export default function App() {
  const [q, setQ] = useState("python functions");
  const [cat, setCat] = useState("");
  const [page, setPage] = useState(1);
  const [data, setData] = useState(null);
  const [bench, setBench] = useState(null);
  const [history, setHistory] = useState([]);
  const search = async (p = 1) => {
    setPage(p);
    const r = await fetch(`${API}/search?q=${encodeURIComponent(q)}&category=${cat}&page=${p}&size=5`);
    setData(await r.json());
    const h = await fetch(`${API}/history`); setHistory((await h.json()).history);
  };
  const feedback = async (id, helpful) => {
    await fetch(`${API}/feedback`, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ article_id: id, helpful }) });
    search(page);
  };
  const runBench = async () => { const r = await fetch(`${API}/benchmark`); setBench(await r.json()); };
  return (<div style={{ maxWidth: 800, margin: "auto", padding: 20, fontFamily: "sans-serif" }}>
    <h1>🔍 Semantic Search Engine</h1>
    <input value={q} onChange={e => setQ(e.target.value)} placeholder="Search articles..." style={{ width: "60%", padding: 10 }} />
    <select value={cat} onChange={e => setCat(e.target.value)} style={{ padding: 10, marginLeft: 8 }}>
      <option value="">All Categories</option><option>Python</option><option>Web</option><option>Frontend</option><option>Database</option><option>DevOps</option><option>AI</option><option>Search</option>
    </select>
    <button onClick={() => search(1)} style={{ padding: 10, marginLeft: 8 }}>Search</button>
    <button onClick={runBench} style={{ padding: 10, marginLeft: 8 }}>Benchmark</button>
    {bench && <div style={{ background: "#eef", padding: 12, marginTop: 12 }}><b>Benchmark Accuracy: {bench.accuracy * 100}%</b>{bench.cases.map((c, i) => <div key={i}>{c.query} → top #{c.top_id} {c.correct ? "✅" : "❌"} (score {c.top_score})</div>)}</div>}
    {data && <p>{data.total} results - Page {data.page}</p>}
    {data?.results.map(a => <div key={a.id} style={{ border: "1px solid #ddd", padding: 12, marginTop: 10 }}>
      <b>{a.title}</b> <span>[{a.category}] Score: {a.score}</span><p>{a.content}</p>
      <small>Keyword: {a.keyword_score} | Semantic: {a.semantic_score} | 👍 {a.feedback.up} 👎 {a.feedback.down}</small><br />
      <button onClick={() => feedback(a.id, true)}>👍 Helpful</button><button onClick={() => feedback(a.id, false)} style={{ marginLeft: 8 }}>👎 Not Helpful</button>
    </div>)}
    {data && <div style={{ marginTop: 12 }}><button disabled={page <= 1} onClick={() => search(page - 1)}>Prev</button><span style={{ margin: 10 }}>Page {page}</span><button disabled={page * 5 >= data.total} onClick={() => search(page + 1)}>Next</button></div>}
    <h3>Search History</h3>{history.slice(-5).map((h, i) => <div key={i}>{h.query} - {h.results} results</div>)}
  </div>);
}