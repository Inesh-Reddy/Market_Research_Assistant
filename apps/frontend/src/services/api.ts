const BASE = import.meta.env.VITE_API_BASE || "http://localhost:8000";
export async function postChat(question: string, conversationId?: string) {
  const r = await fetch(`${BASE}/api/v1/chat`, { method: "POST", headers: {"Content-Type":"application/json"}, body: JSON.stringify({ question, conversation_id: conversationId || undefined }) });
  if (!r.ok) throw new Error(`chat ${r.status}: ${await r.text()}`);
  return r.json() as Promise<{execution_id:string;conversation_id:string;status:string}>;
}
export async function getResult(executionId: string) {
  const r = await fetch(`${BASE}/api/v1/executions/${executionId}/result`);
  if (!r.ok) throw new Error(`result ${r.status}`);
  return r.json();
}
export async function getAgents() { const r=await fetch(`${BASE}/api/v1/agents`); return r.json(); }
export function eventsUrl(executionId: string) { return `${BASE}/api/v1/executions/${executionId}/events`; }
