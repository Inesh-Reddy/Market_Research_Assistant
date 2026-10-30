export interface ExecEvent { event_id: string; execution_id: string; conversation_id: string; event_type: string; agent_name?: string|null; timestamp: string; duration_ms?: number|null; payload: Record<string, unknown>; }
export interface AgentInfo { name: string; role: string; tools: string[]; status: string; }
export type AgentStatus = "pending"|"running"|"completed"|"failed"|"retrying";
export interface SourceRef { title: string; url: string; published_at?: string|null; source: string; }
export interface Finding { title: string; detail: string; sources: SourceRef[]; }
export interface FinancialValue { label: string; value?: number|null; currency: string; source: string; market_timestamp?: string|null; retrieved_at: string; }
export interface AgentResult { agent_name: string; status: string; summary: string; findings: Finding[]; sources: SourceRef[]; financials: FinancialValue[]; sentiment?: string|null; error?: string|null; confidence: number; }
export interface ConsolidatedResult { execution_id: string; question: string; ticker?: string|null; final_response: string; agent_results: AgentResult[]; contradictions: string[]; sources: {title:string;url:string;source:string;published_at?:string|null}[]; }
