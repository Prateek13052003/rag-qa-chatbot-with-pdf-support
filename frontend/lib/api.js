const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function uploadPDF(file, sessionId) {
  const formData = new FormData();
  formData.append("file", file);
  formData.append("session_id", sessionId);

  const response = await fetch(`${API_BASE}/upload`, {
    method: "POST",
    body: formData,
  });
  return response.json();
}

export async function sendMessage(message, sessionId) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message, session_id: sessionId }),
  });
  return response.json();
}

export async function getChatHistory(sessionId) {
  const response = await fetch(`${API_BASE}/history/${sessionId}`);
  return response.json();
}
