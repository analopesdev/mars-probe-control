const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  const body = await response.json().catch(() => null);

  if (!response.ok) {
    throw new Error(toErrorMessage(body, response.status));
  }
  return body;
}

// O FastAPI devolve "detail" como texto (nossos erros) ou como lista (erros de validação do Pydantic).
function toErrorMessage(body, status) {
  const detail = body?.detail;
  if (typeof detail === "string") return detail;
  if (Array.isArray(detail)) return detail.map((error) => error.msg).join("; ");
  return `Erro ${status}`;
}

export function launchProbe(x, y, direction) {
  return request("/probes", {
    method: "POST",
    body: JSON.stringify({ x, y, direction }),
  });
}

export function moveProbe(id, commands) {
  return request(`/probes/${id}/commands`, {
    method: "POST",
    body: JSON.stringify({ commands }),
  });
}

export async function listProbes() {
  const body = await request("/probes");
  return body.probes;
}
