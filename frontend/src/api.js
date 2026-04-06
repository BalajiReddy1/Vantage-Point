const API_BASE = '/api';

export async function fetchDashboardData() {
  const res = await fetch(`${API_BASE}/dashboard-data`);
  if (!res.ok) throw new Error(`Failed to fetch dashboard data: ${res.status}`);
  return res.json();
}

export async function generateBrief() {
  const res = await fetch(`${API_BASE}/brief`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to generate brief: ${res.status}`);
  return res.json();
}

export async function askQuestion(query) {
  const res = await fetch(`${API_BASE}/ask`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!res.ok) throw new Error(`Failed to ask: ${res.status}`);
  return res.json();
}

export async function fetchHistory(limit = 10) {
  const res = await fetch(`${API_BASE}/history?limit=${limit}`);
  if (!res.ok) throw new Error(`Failed to fetch history: ${res.status}`);
  return res.json();
}

export async function acknowledgeAlert(alertId) {
  const res = await fetch(`${API_BASE}/alerts/${alertId}/ack`, { method: 'POST' });
  if (!res.ok) throw new Error(`Failed to acknowledge alert: ${res.status}`);
  return res.json();
}

export async function fetchHealth() {
  const res = await fetch(`${API_BASE}/health`);
  if (!res.ok) throw new Error(`API health check failed: ${res.status}`);
  return res.json();
}
