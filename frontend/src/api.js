const BASE_URL = "/api";

async function postJson(path, body) {
  const response = await fetch(`${BASE_URL}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `요청 실패 (${response.status})`);
  }
  return response.json();
}

async function getJson(path) {
  const response = await fetch(`${BASE_URL}${path}`);
  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `요청 실패 (${response.status})`);
  }
  return response.json();
}

export function analyze(payload) {
  return postJson("/analyze", payload);
}

export function getWelcomeUser() {
  return getJson("/welcome-user");
}

export function submitReport(payload) {
  return postJson("/reports", payload);
}
