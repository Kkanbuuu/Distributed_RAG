const ORCHESTRATOR_URL = import.meta.env.VITE_ORCHESTRATOR_URL || '/api';

export async function sendQuery(queryText, topK = 5) {
  const res = await fetch(`${ORCHESTRATOR_URL}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query_text: queryText, top_k: topK }),
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail || `Request failed: ${res.status}`);
  }
  return res.json();
}
