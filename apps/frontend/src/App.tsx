import { useState } from "react";
import ChatPanel from "./components/chat/ChatPanel";
import AgentMonitor from "./components/agents/AgentMonitor";
import TerminalPanel from "./components/terminal/TerminalPanel";
import { useExecutionStream } from "./hooks/useExecutionStream";
import { postChat, getResult } from "./services/api";
import AgentResults from "./components/chat/AgentResults";
import type { ConsolidatedResult } from "./types";
export default function App(){
  const [question,setQuestion]=useState("Give me the latest analysis of Apple stock. Include recent news, financial performance, investor sentiment, and potential risks.");
  const [executionId,setExecutionId]=useState<string|null>(null);
  const [answer,setAnswer]=useState("");
  const [result,setResult]=useState<ConsolidatedResult|null>(null);
  const [busy,setBusy]=useState(false);
  const [err,setErr]=useState("");
  const {events,connected}=useExecutionStream(executionId);
  async function submit(){
    setBusy(true); setErr(""); setAnswer(""); setResult(null);
    try{
      const r=await postChat(question); setExecutionId(r.execution_id);
      const poll=setInterval(async()=>{
        try{ const res=await getResult(r.execution_id); setResult(res); setAnswer(res.final_response||""); setBusy(false); clearInterval(poll);}catch{}
      },2000);
      setTimeout(()=>{clearInterval(poll); setBusy(false);},180000);
    }catch(e){ setErr(String(e)); setBusy(false); }
  }
  return (<div className="min-h-screen p-3 flex flex-col gap-3 max-w-[1500px] mx-auto">
    <header className="flex flex-wrap justify-between gap-2 border-b border-slate-800 pb-2">
      <div><h1 className="font-bold">Financial Intelligence Platform</h1><p className="text-xs text-slate-400">Coordinator → News / Financial / Sentiment · Ollama gemma3:270m · SSE live events {connected?"· connected":""}</p></div>
      <div className="text-xs text-slate-400">Backend :8000 · Frontend :5173 · Ollama :11434</div>
    </header>
    {err && <div className="text-red-300 text-sm border border-red-900 bg-red-950 rounded p-2">{err}</div>}
    <div className="grid lg:grid-cols-2 gap-3"><ChatPanel question={question} setQuestion={setQuestion} onSubmit={submit} busy={busy} answer={answer}/><div className="flex flex-col gap-3"><AgentMonitor events={events}/><div className="border border-slate-700 rounded p-3 bg-slate-950 text-xs text-slate-400">Prompt & tool inspection: expand any event in the log below. Enable LOG_PROMPTS=true in backend .env to include rendered prompts. Secrets are never emitted.</div></div></div>
    <AgentResults result={result}/>
    <TerminalPanel events={events}/>
  </div>);
}
